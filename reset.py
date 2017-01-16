#!/usr/bin/python2.6

import cookielib
import getpass
import httplib
import json
import logging
import logging.handlers
import os
import re
import sys
import tarfile
import time
import threading
import urllib
import urllib2
import urlparse

from datetime import datetime
from HTMLParser import HTMLParser
from optparse import OptionParser
from StringIO import StringIO

from pyVmomi import Vim
from pyVim import connect
from pyVim.task import WaitForTask

import gen_ovfenv

__author__ = "VMware, Inc."
__copyright__ = "Copyright 2015, VMware, Inc."
__version__ = "1.00"

log = None

ROOT_USER = 'root'
PRECONF_PWD = "Passw0rd!"
VIM_VERSION_9 = 'vim.version.version9' # Needed for VSAN

VM_IMAGES_DIR = 'images/'

VCVA_VM_NAME = ['VMware vCenter Server Appliance', 'VCSA', 'VCVA']
VCVA_IMAGES_DIR = VM_IMAGES_DIR + 'vcsa-restore-original/'
VCVA_DEFAULT_PWD = 'vmware'

LOG_INSIGHT_VM_NAME = ['VMware vCenter Log Insight']
LOG_INSIGHT_IMAGES_DIR = VM_IMAGES_DIR + 'log-insight-original/'
LOG_INSIGHT_OVF_PROPS = { 'vm.rootpw' : PRECONF_PWD }

SYSTEM_VMS = VCVA_VM_NAME + LOG_INSIGHT_VM_NAME

DATASTORE_FOLDER_PATH = "https://%s/folder/%s?dcPath=ha-datacenter&dsName="

ESXI_55_U2_BUILD = 2068190
ESXI_55_U1_BUILD = 1623387

MAX_ATTEMPTS = 10

CONFIG_MANIFEST = "Manifest.txt"

VENDOR_OVF_MANIFEST = "manifest.json"

def setupLogger(defaultLevel=logging.DEBUG, syslog=True, sysout=True):
    global log

    formatter = 'Appliance reset: %(asctime)s.%(msecs)03dZ - %(levelname)s %(message)s'

    log = logging.getLogger(__name__)

    if syslog:
        syslogHandler = logging.handlers.SysLogHandler(address = '/dev/log')
        syslogHandler.setFormatter(logging.Formatter(formatter))
        syslogHandler.setLevel(defaultLevel)
        log.addHandler(syslogHandler)

    if sysout:
        sysoutHandler = logging.StreamHandler(sys.stdout)
        sysoutHandler.setFormatter(logging.Formatter(formatter))
        sysoutHandler.setLevel(defaultLevel)
        log.addHandler(sysoutHandler)

    log.setLevel(defaultLevel)

def _checkHostConnection(fn):
    def connChecker(self, *args, **kwargs):
        if not self.hostConn or not self.hostObj:
            raise Exception("No host connection or host object.")
        return fn(self, *args, **kwargs)

    return connChecker

def _linearBackoff(tries=3, backoff=2):
    '''"A decorator that retries the given function.  It will retry if the
    decorated function raises any subclass of Exception.
    '''
    def decoBackoff(fn):
        def fnBackoff(*args, **kwargs):
            import time
            count = 1

            while True:
                try:
                    return fn(*args, **kwargs)
                except Exception, ex:
                    if log.getEffectiveLevel() > logging.INFO:
                        log.warning("Executing '%s' failed (%s).  Attempt %d." %
                                    (fn.__name__, ex.message, count))
                    else:
                        log.info("Executing '%s' failed.  Attempt %d, trying"
                                 " again soon." % (fn.__name__, count))

                if count == tries:
                    raise Exception("Unable to successfully execute '%s'"
                                       " after %d tries.  Reset cannot"
                                       " continue." % (fn.__name__, count))

                time.sleep(backoff * count)
                count += 1

        return fnBackoff
    return decoBackoff

class DataHTMLParser(HTMLParser):
    def __init__(self, searchString):
        HTMLParser.__init__(self)
        self.searchString = searchString
        self.results = []

    def handle_data(self, data):
        if data.strip().endswith(self.searchString):
            self.results.append(data)

class HostResetter():
    def __init__(self, hostAddr, passwd, primary=False):
        self.hostAddr = hostAddr
        self.passwd = passwd
        self.primary = primary
        self.hostConn = None
        self.hostObj = None
        self.bootTime = None
        self.resetSuccessful = False

    def connectToHost(self, useDefaultPassword=False):
        if useDefaultPassword:
            pwd = PRECONF_PWD
        else:
            pwd = self.passwd

        self.hostConn = connect.Connect(host=self.hostAddr, user=ROOT_USER,
                pwd=pwd, version=VIM_VERSION_9)
        self.hostObj = self.hostConn.content.rootFolder.childEntity[0].hostFolder.childEntity[0].host[0]

    @_checkHostConnection
    def powerOffAndDestroyVMs(self, vmNames):
        log.debug("Searching for %s on %s", vmNames, self.hostAddr)
        host = self.hostObj

        destroyedVMs = []

        # Look at all the VMs, destroy any that are in the vmNames list
        vm = None
        vmName = None
        for vm in host.vm:
            log.debug("Looking at VM: %s", vm.name)
            if vm.name in vmNames:
                vmName = vm.name

                if vm.runtime.powerState != Vim.VirtualMachine.PowerState.poweredOff:
                    log.debug("  Powering off VM.")
                    t = WaitForTask(vm.PowerOffVM_Task())
                log.debug("  Destroying VM.")
                t = WaitForTask(vm.Destroy_Task())

                destroyedVMs.append(vmName)

    @_checkHostConnection
    def powerOffAndDestroyAllVMs(self):
        if not self.hostObj.vm:
            log.debug("No VMs found on host %s; nothing to destroy.",
                    self.hostAddr)
            return

        log.warning("DESTROYING ALL VMs ON %s: %s", self.hostAddr, [i.name for i
            in self.hostObj.vm])
        log.warning("5 SECONDS UNTIL DESTROYING VMS...")
        time.sleep(5)
        for vm in self.hostObj.vm:
            if vm.runtime.powerState != Vim.VirtualMachine.PowerState.poweredOff:
                log.debug("  Powering off VM: %s", vm.name)
                t = WaitForTask(vm.PowerOffVM_Task())
            log.debug("  Destroying VM: %s", vm.name)
            t = WaitForTask(vm.Destroy_Task())

    @_checkHostConnection
    @_linearBackoff(backoff=10)
    def removeHostFromVSANCluster(self):
        log.debug("Removing host %s from VSAN cluster.", self.hostAddr)
        vsanConfig = Vim.vsan.host.ConfigInfo()
        vsanConfig.enabled = False
        t = self.hostObj.configManager.vsanSystem.UpdateVsan_Task(vsanConfig)
        return WaitForTask(t)

    @_checkHostConnection
    def addHostToVSANCluster(self, uuid=None):
        log.debug("Creating VSAN cluster on host %s." % self.hostAddr)
        vsanConfig = Vim.vsan.host.ConfigInfo()
        vsanClusterInfo = Vim.vsan.host.ConfigInfo.ClusterInfo()

        vsanConfig.clusterInfo = vsanClusterInfo
        vsanConfig.enabled = True

        t = self.hostObj.configManager.vsanSystem.UpdateVsan_Task(vsanConfig)
        return WaitForTask(t)

    @_checkHostConnection
    def putHostInMaintenanceMode(self):
        if not self.hostObj.runtime.inMaintenanceMode:
            log.debug("Putting host %s in maintenance mode.", self.hostAddr)
            t = WaitForTask(self.hostObj.EnterMaintenanceMode_Task(timeout=0))
        else:
            log.debug("Host %s is already in maintenance mode.", self.hostAddr)

    @_checkHostConnection
    def resetHost(self):
        for ds in self.hostObj.datastore:
            # Break on the VMFS datastore, not the VSAN one; there can be only
            # one VMFS datastore.
            if ds.summary.type == 'VMFS':
                break

        dsName = ds.name
        hostHttpOpener = self.createESXiBrowserOpener()

        configBundle = self.getConfigBundle(hostHttpOpener, dsName)
        configBundle = self.normalizeConfigBundleVersion(configBundle)
        ctxt = self.putConfigBundle(hostHttpOpener, configBundle)

        log.debug("Restoring backup config and rebooting host: %s", self.hostAddr)
        firmwareSys = self.hostObj.configManager.firmwareSystem
        firmwareSys.RestoreFirmwareConfiguration(force=False)

        # Flush out any, now stale, host connection (and related) objects.
        self.hostConn = None
        self.hostObj = None

    @_checkHostConnection
    def deployVMFromOvf(self, vmName, ovfImageLocation, powerOn=False):
        log.info("Deploying VM: %s from %s.", vmName, ovfImageLocation)

        content = self.hostConn.content

        ovfManager = content.ovfManager
        datacenter = content.rootFolder.childEntity[0]
        vmFolder = datacenter.vmFolder
        resPool = datacenter.hostFolder.childEntity[0].resourcePool
        datastores = datacenter.datastore

        # The vsanDS is where we want to deploy the VM to;
        # vmfsDS is where we will grab the OVF files from
        vsanDS = None
        vmfsDS = None

        for datastore in datastores:
            if datastore.summary.type == 'vsan':
                vsanDS = datastore
            elif datastore.summary.type == 'VMFS':
                vmfsDS = datastore

        if not vsanDS or not vmfsDS:
            raise Exception("Could not find either a VSAN or a VMFS datastore on" \
                    " host %s." % self.hostAddr)

        ovfFile = self.retrieveOvfFile(vmfsDS, ovfImageLocation)

        if not ovfFile:
            raise Exception("OVF file is empty!")

        specParams = Vim.OvfManager.CreateImportSpecParams(entityName=vmName, diskProvisioning='thin')
        spec = ovfManager.CreateImportSpec(ovfFile, resPool, vsanDS, specParams)
        lease = resPool.ImportVApp(spec.importSpec, vmFolder)

        # Linear backoff to wait for the lease.
        for att in range(MAX_ATTEMPTS):
            if lease.state in ('ready', 'error'):
                break
            log.debug("Waiting for lease to be ready ...")
            time.sleep(att)

        if lease.state == 'error':
            log.error("Lease failed...")
            raise lease.info.error

        vm = self.uploadVMFiles(spec, lease, vmfsDS, ovfImageLocation)

        if powerOn:
            log.debug("Powering on VM: %s", vmName)
            WaitForTask(vm.PowerOnVM_Task())

        return vm

    @_checkHostConnection
    def restartService(self, serviceName):
        log.debug("Restarting service '%s' on host %s.", serviceName, self.hostAddr)
        serviceSystem = self.hostObj.configManager.serviceSystem

        serviceSystem.RestartService(serviceName)

    @_checkHostConnection
    def executeOnGuest(self, vm, username, password, program, args):
        log.debug("Executing '%s' with arguments '%s' on %s.", program, args,
                vm.name)
        auth = Vim.NamePasswordAuthentication()
        auth.username = username
        auth.password = password

        guestProgSpec = Vim.GuestProgramSpec()
        guestProgSpec.programPath = program
        guestProgSpec.arguments = args

        procMgr = self.hostConn.content.guestOperationsManager.processManager
        procMgr.StartProgramInGuest(vm, auth, guestProgSpec)

    def findVendorOvfFolders(self, datastore):
        class VendorOVFFolderHTMLParser(HTMLParser):
            def __init__(self):
                HTMLParser.__init__(self)
                self.vendorFolders = []

            def handle_data(self, data):
                if re.search(r'vendor[0-9]+-original/', data.strip()):
                    self.vendorFolders.append(data)


        opener = self.createESXiBrowserOpener()
        browserPath = DATASTORE_FOLDER_PATH + datastore.name

        vendorOVFFinder = VendorOVFFolderHTMLParser()
        ctxt = opener.open(browserPath % (self.hostAddr, VM_IMAGES_DIR))

        vendorOVFFinder.feed(ctxt.read())

        vendorFolders = vendorOVFFinder.vendorFolders
        log.debug("Found vendor folders: %s", vendorFolders)

        res = []

        for vendorFolder in vendorFolders:
            manifestFinder = DataHTMLParser(VENDOR_OVF_MANIFEST)

            vendorDir = VM_IMAGES_DIR + vendorFolder

            ctxt = opener.open(browserPath % (self.hostAddr, vendorDir))

            manifestFinder.feed(ctxt.read())
            manifestFile = manifestFinder.results

            if manifestFile:
                log.debug("Found %s in '%s'", manifestFile, vendorDir)
            else:
                log.error("No %s found in '%s'. Not deploying VM in folder.",
                          manifestFile, vendorDir)
                break

            manifestFileContext = opener.open(browserPath % (self.hostAddr,
                vendorDir + VENDOR_OVF_MANIFEST))

            try:
                manifestFileContents = manifestFileContext.read()
                manifestFileContents = json.loads(manifestFileContents)
            except:
                log.error("Invalid JSON file (%s) in %s.", manifestFile,
                    vendorDir)
                break

            res.append((vendorDir, manifestFileContents))

        return res

    def waitForHost(self, timeout=30, rebootTimeout=720):
        log.debug("Waiting for host '%s'.", self.hostAddr)

        rebootTime = datetime.utcnow()
        time.sleep(timeout)

        while (datetime.utcnow() - rebootTime).seconds < rebootTimeout:
            curTime = datetime.utcnow()
            try:
                # Let's try connecting with the default password.
                log.info("Trying to connect to %s ...", self.hostAddr)
                self.connectToHost(useDefaultPassword=True)
                self.resetSuccessful = True
                log.info("Connection to host %s successful.", self.hostAddr)
                return
            except Vim.fault.HostConnectFault:
                log.info("Host %s not yet available, still waiting ...",
                        self.hostAddr)
                time.sleep(timeout)
            except Vim.fault.InvalidLogin:
                # Let the caller invoke reset again.
                log.error("Host %s was not correctly reset (based on password).",
                        self.hostAddr)
                self.resetSuccessful = False
                return

        log.error("Unable to contact '%s' after %s seconds.", self.hostAddr,
            rebootTimeout)

    def injectOvfEnvironment(self, vm, ovfProperties):
        ovfEnv = gen_ovfenv.generateOvfEnvXml(ovfProperties)
        log.debug("Setting properties for VM: '%s' to %s", vm.name,
                ovfProperties)

        cs = Vim.vm.ConfigSpec(
                extraConfig=[
                    Vim.option.OptionValue(
                        key="guestinfo.ovfEnv",
                        value=ovfEnv)])

        t = vm.Reconfigure(cs)
        log.info("Reconfiguring VM '%s' OVF environment: %s.", vm.name,
                WaitForTask(t))

        return vm

    def uploadVMFiles(self, spec, lease, ovfDSSource, ovfImageLocation):
        totalBytes = sum([fileItem.size for fileItem in spec.fileItem])
        bytesSent = 0

        vm = lease.info.entity
        opener = self.createESXiBrowserOpener()

        for devUrl in lease.info.deviceUrl:
            for fileItem in spec.fileItem:
                if devUrl.importKey != fileItem.deviceId:
                    continue

                filePath = os.path.join(ovfImageLocation, fileItem.path)

                fileURL = DATASTORE_FOLDER_PATH + ovfDSSource.name
                fileURL = fileURL % (self.hostAddr, urllib.quote(filePath))

                ctxt = opener.open(fileURL)

                postUrl = devUrl.url.replace('*', self.hostAddr)

                log.debug("Sending '%s' to '%s'." % (fileURL, postUrl))
                parsedUrl = urlparse.urlparse(postUrl)
                conn = httplib.HTTPSConnection(parsedUrl.netloc)
                conn.putrequest('POST', parsedUrl.path)
                conn.putheader('content-length', fileItem.size)
                conn.endheaders()

                totalLoops = 0
                while True:
                    bits = ctxt.read(128 * 1024)
                    if not bits:
                        break
                    conn.send(bits)
                    bytesSent += len(bits)

                    if (totalLoops % 128) == 0:
                        progress = int(round((float(bytesSent) / float(totalBytes)) * 100))

                    lease.Progress(max(1, progress))
                    log.debug("Current progress: %s", progress)
                    totalLoops += 1

                conn.close()

        lease.Progress(100)
        lease.Complete()

        return vm

    def retrieveOvfFile(self, datastore, ovfImageLocation):
        opener = self.createESXiBrowserOpener()

        browserPath = DATASTORE_FOLDER_PATH + datastore.name
        ovfFilePath = self.findOvfFile(opener, browserPath % (self.hostAddr,
                                                              ovfImageLocation))

        ovfFileContext = opener.open(browserPath % (self.hostAddr,
            urllib.quote(ovfImageLocation + ovfFilePath)))

        ovfFileContents = ovfFileContext.read()
        return ovfFileContents

    def createESXiBrowserOpener(self):
        folderBrowsePath = "https://%s/folder"

        cj = cookielib.CookieJar()
        cookieProc = urllib2.HTTPCookieProcessor(cj)

        authHandler = urllib2.HTTPBasicAuthHandler()
        authHandler.add_password(realm="VMware HTTP server",
                uri=folderBrowsePath % self.hostAddr,
                user=ROOT_USER,
                passwd=self.passwd)

        opener = urllib2.build_opener(authHandler, cookieProc)

        return opener

    def findOvfFile(self, opener, browserPath):
        class OVFDataHTMLParser(HTMLParser):
            def __init__(self):
                HTMLParser.__init__(self)
                self.ovfFile = None

            def handle_data(self, data):
                if data.strip().endswith('.ovf'):
                    self.ovfFile = data

        ovfFinder = OVFDataHTMLParser()
        ctxt = opener.open(browserPath)

        ovfFinder.feed(ctxt.read())

        return ovfFinder.ovfFile

    def getConfigBundle(self, opener, dsName):
        configBundlePath = \
            "https://%s/folder/reset/configBundle.tgz?dcPath=ha-datacenter&dsName=%s"

        ctxt = opener.open(configBundlePath % (self.hostAddr, dsName))
        log.debug("Fetching configBundle from %s", ctxt.geturl())

        return ctxt.read()

    def putConfigBundle(self, opener, configBundle):
        firmwareSys = self.hostObj.configManager.firmwareSystem

        postUrl = firmwareSys.QueryFirmwareConfigUploadURL()
        postUrl = postUrl.replace('*', self.hostAddr, 1)
        postUrl = postUrl.replace('http', 'https', 1)

        log.debug("Uploading configBundle to: %s", postUrl)
        req = urllib2.Request(postUrl, configBundle,
                              {'content-type': 'application/octet-stream',
                               'content-length': len(configBundle)})

        req.get_method = lambda: 'PUT'
        ctxt = opener.open(req)
        return ctxt

    def normalizeConfigBundleVersion(self, configBundle):
        configStringIO = StringIO(configBundle)

        newConfigStringIO = StringIO()
        newConfigTar = tarfile.open(mode='w:gz', fileobj=newConfigStringIO)

        configTar = tarfile.open(fileobj=configStringIO)
        for member in configTar.getmembers():
            if member.name == CONFIG_MANIFEST:
                fp = configTar.extractfile(member)
                fpCont = fp.read()

                # XXX: The bundle may not have been built from Update 1
                # XXX: Find the actual version and replace it with that
                hostBuildNumber = self.hostObj.summary.config.product.build

                # XXX: This check is not sufficient in the case of ESXi version
                # upgrades.  The version should ideally be checked first.
                if hostBuildNumber >= ESXI_55_U1_BUILD \
                        and hostBuildNumber < ESXI_55_U2_BUILD:
                    fpCont = fpCont.replace("5.5.0 Update 1", "5.5.0 Update 1")
                elif hostBuildNumber >= ESXI_55_U2_BUILD:
                    fpCont = fpCont.replace("5.5.0 Update 1", "5.5.0 Update 2")
                else:
                    raise Exception("ESXi build number is invalid.")

                member.size = len(fpCont)
                newConfigTar.addfile(member, StringIO(fpCont))
            else:
                fp = configTar.extractfile(member)
                newConfigTar.addfile(member, StringIO(fp.read()))

        newConfigTar.close()

        newConfigContents = newConfigStringIO.getvalue()
        return newConfigContents

def enableIvyBridgeEVC(vm):
    vmHWSpec = Vim.vm.ConfigSpec()

    vmCpuId01InfoSpec = Vim.vm.ConfigSpec.CpuIdInfoSpec()

    int01CpuIdInfo = Vim.host.CpuIdInfo()
    int01CpuIdInfo.level = 1
    int01CpuIdInfo.eax = "00000000000000100000011010100010"
    int01CpuIdInfo.ecx = "01110110100110101110001000111111"
    int01CpuIdInfo.edx = "10001111111010111111101111111111"

    vmCpuId01InfoSpec.info = int01CpuIdInfo
    vmCpuId01InfoSpec.operation = Vim.option.ArrayUpdateSpec.Operation.edit

    vmCpuId81InfoSpec = Vim.vm.ConfigSpec.CpuIdInfoSpec()

    int81CpuIdInfo = Vim.host.CpuIdInfo()
    int81CpuIdInfo.level = -2147483647
    int81CpuIdInfo.ecx = "00000000000000000000000000000001"
    int81CpuIdInfo.edx = "00101000000100000000100000000000"

    vmCpuId81InfoSpec.info = int81CpuIdInfo
    vmCpuId81InfoSpec.operation = Vim.option.ArrayUpdateSpec.Operation.edit

    vmHWSpec.cpuFeatureMask.append(vmCpuId01InfoSpec)
    vmHWSpec.cpuFeatureMask.append(vmCpuId81InfoSpec)

    log.info("Enabling Ivy Bridge EVC for VM: %s", vm.config.name)
    WaitForTask(vm.ReconfigVM_Task(vmHWSpec))

def upgradeVMHardware(vm, hwVersion=None):
    log.info("Upgrading hardware on VM: %s", vm.config.name)
    try:
        if hwVersion:
            WaitForTask(vm.UpgradeVM_Task(version=hwVersion))
        else:
            WaitForTask(vm.UpgradeVM_Task())
    except:
        log.exception("Upgrading VM's hardware failed.")

def parseArgs():
    usage = "Usage: %prog [options]"
    parser = OptionParser(usage)

    parser.add_option('-v', "--verbose",
                      action="store_true", dest="verbose")
    parser.add_option("--version",
                      action="store_true", dest="version",
                      help="Displays the version number.")
    parser.add_option('-f', "--primary",
                      action="store", dest="primaryNode", metavar="PRIMARY",
                      help="The primary node of the appliance.  This node" \
                        " will be removed from the VSAN cluster, reset, and the" \
                        " VCVA VM redeployed on this node.")
    parser.add_option('-a', "--additional",
                      action="append", dest="additionalNodes",
                      metavar="ADDITIONAL", help="Non-primary nodes of the" \
                        " appliance to be reset.  Specify once for each node.")
    parser.add_option('-p', "--password",
                      action="store", dest="password", metavar="PASSWORD",
                      help="The password of the post-configured appliance." \
                        " Prompts if not supplied.")
    parser.add_option('-d', "--destroySystemVMs",
                      action="store_true", dest="destroySystemVMs",
                      help="Destroy any initial system VMs (VCVA, Log Insight)," \
                        " if found.")
    parser.add_option("--onlyRegeneratePrimary",
                      action="store_true", dest="onlyRegenerate",
                      help="Only regenerates the primary host.  Does not destroy" \
                        " VMs or reset the host.  Must be passed in with '-f'." \
                        " Not usable with '-a', '-d', '--destroyAllVMs' flags.")
    parser.add_option("--destroyAllVMs",
                      action="store_true", dest="destroyAllVMs", \
                      help="(DESTRUCTIVE) Destroys all VMs.  Must be supplied" \
                        " with --destroySystemVMs.")
    parser.add_option('-r', "--rpm",
                      action="store", dest="rpmFile", metavar="FILE",
                      help="(UNSUPPORTED) If provided, this RPM will be" \
                        " uploaded onto the deployed VCVA.")

    opts, _ = parser.parse_args()

    if opts.version:
        print "%s: Version %s" % (sys.argv[0], __version__)
        sys.exit(0)

    if not opts.primaryNode and not opts.additionalNodes:
        print >> sys.stderr, "Must provide at least one of PRIMARY node, or" \
            " ADDITIONAL node."
        parser.print_help()
        sys.exit(1)

    if opts.onlyRegenerate and (opts.additionalNodes or opts.destroySystemVMs
            or opts.destroyAllVMs or not opts.primaryNode):
        print >> sys.stderr, "--onlyRegeneratePrimary passed in.  Please run" \
            " with '-h' for correct usage."
        sys.exit(1)

    if opts.destroyAllVMs and not opts.destroySystemVMs:
        print >> sys.stderr, "--destroyAllVMs must be passed in with" \
            " --destroySystemVMs."
        sys.exit(1)

    if not opts.password:
        opts.password = getpass.getpass("Post-configuration Password: ")

    return opts

def main():
    opts = parseArgs()

    if opts.verbose:
        setupLogger(syslog=False)
        log.info("Verbose mode active.  Setting log level to DEBUG.")
    else:
        setupLogger(defaultLevel=logging.INFO, syslog=False)

    primaryNode = None
    additionalNodes = []

    allNodes = []

    if opts.primaryNode:
        log.info("Primary node supplied: %s", opts.primaryNode)
        primaryNode = HostResetter(opts.primaryNode, opts.password,
            primary=True)
        primaryNode.connectToHost()
        allNodes.append(primaryNode)
    if opts.additionalNodes:
        for nodeAddr in opts.additionalNodes:
            log.info("Secondary node supplied: %s", nodeAddr)
            newNode = HostResetter(nodeAddr, opts.password)
            newNode.connectToHost()
            additionalNodes.append(newNode)

        allNodes = additionalNodes + allNodes

    if not opts.onlyRegenerate:
        # Store the boot time of the hosts for use to determine whether the host
        # as finished rebooting.

        allVMs = []
        for node in allNodes:
            node.bootTime = node.hostObj.runtime.bootTime
            vmNames = [ i.name for i in node.hostObj.vm ]
            allVMs += vmNames

        if opts.destroySystemVMs and not opts.destroyAllVMs:
            log.warning("Destroying all system VMs: %s.", SYSTEM_VMS)

            for node in allNodes:
                node.powerOffAndDestroyVMs(SYSTEM_VMS)
        elif opts.destroySystemVMs and opts.destroyAllVMs and allVMs:
            log.warning("================================================")
            log.warning("THE FOLLOWING ARE THE CURRENTLY REGISTERED"      )
            log.warning("VIRTUAL MACHINES:"                               )
            log.warning(allVMs)
            log.warning("")
            log.warning("CONTINUING WILL DESTROY ALL VIRTUAL MACHINES"    )
            log.warning("REGISTERED WITH THE APPLIANCE."                  )
            log.warning("================================================")

            confirm = raw_input("CONFIRM (YES/NO): ")
            while confirm != "YES" and confirm != "NO":
                confirm = raw_input("  PLEASE TYPE 'YES' or 'NO': ")

            if confirm != "YES":
                print "EXITING..."
                sys.exit(1)

            for node in allNodes:
                node.powerOffAndDestroyAllVMs()

        # Stop if there are any remaining VMs:
        stopReset = False
        for node in allNodes:
            poweredOnVMs = []
            for vm in node.hostObj.vm:
                stopReset = True
                if vm.runtime.powerState == 'poweredOn':
                    poweredOnVMs.append(vm.name)

            if poweredOnVMs:
                log.warning("Host %s still has powered on VMs: %s",
                        node.hostAddr, poweredOnVMs)

            log.info("Host %s has VMs %s remaining.", node.hostAddr, [i.name for i in
                node.hostObj.vm])

        if stopReset:
            log.error("Please clear out all VMs before continuing.")
            sys.exit(1)

        time.sleep(10)

        log.info("Removing hosts from VSAN cluster.")
        for node in allNodes:
            node.removeHostFromVSANCluster()

        log.info("Putting hosts in maintenance mode.")
        for node in allNodes:
            node.putHostInMaintenanceMode()

        time.sleep(10)

        log.info("Resetting and rebooting hosts.")
        for node in allNodes:
            node.resetHost()

        log.info("Waiting for hosts to finish rebooting to confirm reset ...")
        threads = []
        for node in allNodes:
            t = threading.Thread(target=node.waitForHost)
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        # XXX: This really, really, really should be in its own function...
        failedNodes = []
        for node in allNodes:
            if not node.resetSuccessful:
                log.warning("Host %s was not successfully reset.  Retrying.",
                        node.hostAddr)
                failedNodes.append(node)

        if failedNodes:
            # We need this sleep to let the host settle down.
            log.info("Attempting to reset failed nodes again ...")
            time.sleep(30)

            for node in failedNodes:
                # If the reset failed, then the host *must* be in maintenance
                # mode.
                node.connectToHost()
                t = WaitForTask(node.hostObj.ExitMaintenanceMode_Task(timeout=0))
                node.resetHost()

            log.info("Waiting for hosts to finish rebooting to confirm reset ...")
            threads = []
            for node in failedNodes:
                t = threading.Thread(target=node.waitForHost)
                threads.append(t)
                t.start()

            for t in threads:
                t.join()

    if primaryNode:
        log.info("Regenerating VSAN and VMs on primary node (%s).  Assuming" \
            " default password.", opts.primaryNode)
        primaryNode = HostResetter(primaryNode.hostAddr, PRECONF_PWD, True)
        primaryNode.connectToHost()

        primaryNode.addHostToVSANCluster()

        vcvaVM = primaryNode.deployVMFromOvf(VCVA_VM_NAME[0], VCVA_IMAGES_DIR,
                False)

        upgradeVMHardware(vcvaVM)

        log.info("Reconfiguring VCVA VM.")
        try:
            vmHWSpec = Vim.vm.ConfigSpec()

            vmHWSpec.numCPUs = 4
            vmHWSpec.memoryMB = 16384

            WaitForTask(vcvaVM.ReconfigVM_Task(vmHWSpec))

            enableIvyBridgeEVC(vcvaVM)
        except:
            log.exception("Reconfiguring VM's hardware failed.")

        log.debug("Powering on VM: %s", vcvaVM.config.name)
        WaitForTask(vcvaVM.PowerOnVM_Task())

        try:
            logInsightVM = primaryNode.deployVMFromOvf(LOG_INSIGHT_VM_NAME[0],
                    LOG_INSIGHT_IMAGES_DIR)
            primaryNode.injectOvfEnvironment(logInsightVM,
                    LOG_INSIGHT_OVF_PROPS)
            upgradeVMHardware(logInsightVM)
            enableIvyBridgeEVC(logInsightVM)
        except:
            log.exception("Failed to deploy Log Insight VM.")

        try:
            content = primaryNode.hostConn.content
            datacenter = content.rootFolder.childEntity[0]
            datastores = datacenter.datastore

            for datastore in datastores:
                if datastore.summary.type == 'VMFS':
                    break

            vendorOVFs = primaryNode.findVendorOvfFolders(datastore)

            for vendorOVF in vendorOVFs:
                vendorOVFLocation = vendorOVF[0]
                vendorOVFMetadata = vendorOVF[1]

                deployedVendorOVF = primaryNode.deployVMFromOvf(vendorOVFMetadata['vmName'],
                        vendorOVFLocation)
                upgradeVMHardware(deployedVendorOVF)
                enableIvyBridgeEVC(deployedVendorOVF)
        except:
            log.exception("Failed to deploy Vendor OVFs.")

        log.info("Restarting 'loudmouth'.")
        primaryNode.restartService('loudmouth')

        log.info("Setting VCVA to autostart.")
        autoStartMgr = primaryNode.hostObj.configManager.autoStartManager
        autoStartCfg = Vim.HostAutoStartManagerConfig()

        autoStartDefs = Vim.AutoStartDefaults()
        autoStartDefs.enabled = True
        autoStartDefs.startDelay = 1

        autoStartPowerInfo = Vim.host.AutoStartManager.AutoPowerInfo()
        autoStartPowerInfo.key = vcvaVM
        autoStartPowerInfo.startAction = 'powerOn'
        autoStartPowerInfo.startDelay = 0
        autoStartPowerInfo.startOrder = 1

        autoStartHBSetting = Vim.AutoStartWaitHeartbeatSetting.no
        autoStartPowerInfo.waitForHeartbeat = autoStartHBSetting

        autoStartCfg.defaults = autoStartDefs
        autoStartCfg.powerInfo.append(autoStartPowerInfo)

        autoStartMgr.ReconfigureAutostart(autoStartCfg)

        log.info("Finalizing settings on VCVA.")

        log.debug("Modifying VCVA's initial network...")
        primaryNode.executeOnGuest(vcvaVM, ROOT_USER, VCVA_DEFAULT_PWD,
                "/opt/vmware/share/vami/vami_set_network",
                "eth0 STATICV4 192.168.10.200 255.255.255.0 192.168.10.254")

        log.debug("Modifying VCVA's password expiry policy...")
        primaryNode.executeOnGuest(vcvaVM, ROOT_USER, VCVA_DEFAULT_PWD,
                "/usr/bin/chage",
                "-I -1 -m 0 -M 99999 -E -1 root")

        log.debug("Changing VCVA's default password...")
        primaryNode.executeOnGuest(vcvaVM, ROOT_USER, VCVA_DEFAULT_PWD,
                "/bin/echo",
                "'%s' | passwd --stdin" % PRECONF_PWD)

if __name__=='__main__':
    main()

