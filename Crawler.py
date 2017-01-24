import urllib2

def get_page(url):
    try:
        return urllib2.urlopen(url).read()
    except:
        return ""

def get_next_target(S):
    start_link = S.find('<a href=')
    if start_link == -1:
        return None, 0
    start_quote = S.find('"', start_link)
    end_quote = S.find('"', start_quote+1)
    url = S [start_quote+1 : end_quote]
    return url, end_quote

def print_all_links(x):
    while True:
        url, endpos = get_next_target(x)
        if url:
            print url
            x = x[endpos:]
        else:
            break

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

#page = get_page('https://www.udacity.com/cs101x/index.html')
links = get_all_links('https://www.udacity.com/cs101x/index.html')
print links
