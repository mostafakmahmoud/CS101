import urllib2


#def get_page(url):
#    try:
#        print urllib.urlopen(url).read()
#    except:
#        return ""

page = 'https://www.udacity.com/cs101x/index.html'
print urllib2.urlopen(page).read()
