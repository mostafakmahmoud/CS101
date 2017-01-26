# Modify the crawl_web procedure to take a second parameter,
    # max_depth, that limits the depth of the search.  We can
    # define the depth of a page as the number of links that must
    # be followed to reach that page starting from the seed page,
    # that is, the length of the shortest path from the seed to
    # the page.  No pages whose depth exceeds max_depth should be
    # included in the crawl.
    # For example, if max_depth is 0, the only page that should
    # be crawled is the seed page. If max_depth is 1, the pages
    # that should be crawled are the seed page and every page that
    # it links to directly. If max_depth is 2, the crawl should
    # also include all pages that are linked to by these pages.
    # Note that the pages in the crawl may be in any order.
import urllib2

def crawl_web(seed, max_depth):
    tocrawl = [seed]
    crawled = []
    final_list = []
    i = 0
    depth_counter = 0
    while i < len(tocrawl):
        if tocrawl[i] not in crawled:
            crawled.append(tocrawl[i])
            tocrawl = tocrawl + get_all_links(tocrawl[i])
            i = i+1
        else:
            i = i+1
    return final_list
    depth_counter = depth_counter + 1


    page = tocrawl.pop()
    if page not in crawled:

        union(tocrawl, get_all_links(get_page(page)))
        crawled.append(page)

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

def union(a,b):
    for i in b:
        if i not in a:
            a.append(i)
    return a

crawl_web('https://www.udacity.com/cs101x/index.html')
