import urllib2

def crawl_web(seed): #returns index, graph of outlinks
    tocrawl = [seed] #pages to be crawled starting with seed page
    crawled = [] #Keeping track of crawled pages
    index = {} #our index of pages and keywords
    graph = {} #Urank - {url:[list of pages it links to]}
    while tocrawl: #while there are pages left in tocrawl
        page = tocrawl.pop() #get the last page from tocrawl
        if page not in crawled: #check if its in crawled pages
            content = get_page(page) #get the content
            add_page_to_index(index, page, content) #updates index with words and url
            outlinks = get_all_links(content) #gets all links from the content
            graph[page] = outlinks
            union (tocrawl, outlinks) #combines tocrawl and new outlinks.
            crawled.append(page) #adds the crawled page to crawled list.
    return index, graph

def compute_ranks(graph):
    d = 0.8 #damping factor
    t = 0 #time step
    numloops = 10 #Number of times we will go through relaxation
    ranks = {}
    npages = len(graph) #Number of pages that we crawled

    for pages in graph: #initialize each page.
        ranks[page] = 1.0/ npages #maps each page to its current rank.

    #Go through the number of times of numloops.
    #Each time through this loop:
        #update new ranks based on the formula using old ranks.
    #end of the loop make ranks hold new ranks.
    for i in range(0, numloops):
        newranks = {}
        for page in graph:
            newrank = (1-d) / npages
            for node in graph:
                if page in graph[node]:
                    newrank = newrank + d * (ranks[nodes]/ len(graph[node]))
            newranks[page] = newrank
        ranks = newranks
        return ranks


def get_all_links(page):
    list1 = []
    while True:
        url, endpos = get_next_target(page)
        if url:
            list1.append(url)
            page = page[endpos:]
        else:
            break
    return list1

def get_next_target(page):
    start_link = page.find('<a href=')
    if start_link == -1:
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote+1)
    url = page[start_quote+1 : end_quote]
    return url, end_quote

def get_page(url):
    try:
        return urllib2.urlopen(url).read()
    except:
        return ""

def union(p,q):
    for e in q:
        if e not in p:
            p.append(e)
    return p

def add_to_index(index, keyword, url):
    #look if keyword is already in index, add url to list of urls.
    if keyword in index:
        index[keyword].append(url)
    else:
        #if not found, add new entry.
        index[keyword] = [url]

def lookup(index, keyword):
    if keyword in index:
        return index[keyword]
    else:
        return None

def add_page_to_index(index,url,content):
    words = content.split()
    for word in words:
        add_to_index(index, word, url)

index, graph = crawl_web('https://www.udacity.com/cs101x/urank/index.html')
#print index
print graph
