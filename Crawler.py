import urllib2

def crawl_web(seed):
    tocrawl = [seed]
    crawled = []
    index = []
    while tocrawl:
        page = tocrawl.pop()
        if page not in crawled:
            content = get_page(page)
            add_page_to_index(index, page, content)
            union (tocrawl, get_all_links(content))
            crawled.append(page)
    return index

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
    for entry in index:
        if entry[0] == keyword:
            entry[1].append(url)
            return
    #if not found, add new entry.
    index.append([keyword, [url]])

def lookup(index,keyword):
    for entry in index:
        if entry[0] ==  keyword:
            return entry[1]
    return []

def add_page_to_index(index,url,content):
    words = content.split()
    for word in words:
        add_to_index(index, word, url)

print crawl_web('https://www.udacity.com/cs101x/index.html')
