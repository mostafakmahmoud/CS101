import urllib2

def crawl_web(seed, maxpages):
    tocrawl = [seed]
    crawled = []
    i = 0
    while i < len(tocrawl) and len(crawled)<maxpages:
        if tocrawl[i] not in crawled:
            crawled.append(tocrawl[i])
            tocrawl = tocrawl + get_all_links(tocrawl[i])
            i = i+1
        else:
            i = i+1
    return crawled

def get_all_links(x):
    list1 = []
    S = get_page(x)
    while True:
        url, endpos = get_next_target(S)
        if url:
            list1.append(url)
            S = S[endpos:]
        else:
            break
    return list1

def get_next_target(S):
    start_link = S.find('<a href=')
    if start_link == -1:
        return None, 0
    start_quote = S.find('"', start_link)
    end_quote = S.find('"', start_quote+1)
    url = S [start_quote+1 : end_quote]
    return url, end_quote

def get_page(url):
    try:
        return urllib2.urlopen(url).read()
    except:
        return ""

print crawl_web('http://www.tesla.com',10)
