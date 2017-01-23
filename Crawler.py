page = '''<html>
    <body>
    This is a test page for learning to crawl!
    <p>
    It is a good idea to
    <a href="http://www.udacity.com/cs101x/crawling.html">learn to crawl</a>
    before you try to
    <a href="http://www.udacity.com/cs101x/walking.html">walk</a> or
    <a href="http://www.udacity.com/cs101x/flying.html">fly</a>.
    </p>
    </body>
    </html>
    '''

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
    while True:
        url, endpos = get_next_target(x)
        if url:
            list1.append(url)
            x = x[endpos:]
        else:
            break
    return list1

links = get_all_links(page)
print links[1]
