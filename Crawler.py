#Basic Web Crawler program in python.
#Course CS101 - Introduction to Computer Science

import urllib2 #for function get_page

def crawl_web(seed):
    #Crawler function that starts from a seed page
    #Returns an index of words and urls, and graph of outlinks.
    tocrawl = [seed] #pages to be crawled starting with seed page
    crawled = [] #Keeping track of crawled pages
    index = {} #Our index of pages and keywords
    graph = {} #Urank - {url:[list of urls it links to]}
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
    #Ranks webpages.
    #Rank is based on number of links leading to that page and rank of the link origin.

    d = 0.8 #damping factor
    t = 0 #time step
    numloops = 10 #Number of times we will go through relaxation
    ranks = {}
    npages = len(graph) #Number of pages that we crawled
    for pages in graph: #initialize each page.
        ranks[page] = 1.0/ npages #maps each page to its current rank.
    for i in range(0, numloops): #Go through the number of times of numloops.
        newranks = {}
        for page in graph: #update new ranks based on the formula using old ranks.
            newrank = (1-d) / npages
            for node in graph:
                if page in graph[node]:
                    newrank = newrank + d * (ranks[nodes]/ len(graph[node]))
            newranks[page] = newrank
        ranks = newranks #Assign new ranks to ranks at the end of each loop.
        return ranks

def get_all_links(page):
    #Goes through a webpage, calls get_next_target until no more urls left in the page.
    #Returns a list of urls from that page.
    list1 = []
    while True:
        #get url and endposition, append the url to list, page starts from end position.
        url, endpos = get_next_target(page)
        if url:
            list1.append(url)
            page = page[endpos:]
        else:
            break
    return list1

def get_next_target(page):
    #Extracts the next url from a page.
    #Returns the url and where it stopped in that page.
    start_link = page.find('<a href=') #find the start of a url
    if start_link == -1: #if no result return none.
        return None, 0
    start_quote = page.find('"', start_link)#start of the url
    end_quote = page.find('"', start_quote+1)#end of the url
    url = page[start_quote+1 : end_quote]#get between start and end.
    return url, end_quote

def get_page(url):
    #returns source code for a webpage.
    #depends on urllib2 library
    try:
        return urllib2.urlopen(url).read()
    except:
        return ""

def union(p,q):
    #Union function for lists.
    for e in q:
        if e not in p:
            p.append(e)
    return p

def add_page_to_index(index,url,content):
    #Splits content of a page into keywords (by space characters).
    #Updates the index to include all the words found in that page.
    words = content.split()
    for word in words:
        add_to_index(index, word, url)

def add_to_index(index, keyword, url):
    #Checks if a keyword is already in index.
    #Adds url to list of urls for that word.
    if keyword in index:
        index[keyword].append(url)
        #if not found, create new entry for the word and url.
    else:
        index[keyword] = [url]
    #Doesn't return anything. it Only updates the index.

def lookup(index, keyword):
    #Checks the index for the keyword passed.
    #Returns list of urls associated with that keyword.
    if keyword in index:
        return index[keyword]
    else:
        return None
