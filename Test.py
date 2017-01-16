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

def find_last(text, target):
    while True:
        result = text.find(target)
        if result == -1:
            break
        else:
            x = result
            text.find(target, result+1)
            text = text[result+1:]
    return x

print find_last('aaaa', 'a')
