page = ('<div id="top_bin"><div id="top_content" class="width960">'
'<div class="udacity float-left"><a href="http://udacity.com">')

def get_next_target (S):
    start_link = S.find('<a href=')
    start_quote = S.find('"', start_link)
    end_quote = S.find('"', start_quote+1)
    url = S [start_quote+1 : end_quote]
    return url, end_quote

def rest_of_string (s):
    return s[1:]

def find_second(search, target):
    return search.find(target, search.find(target)+1)
# print find_second('This is Strange Strange','is')

def absolute(x):
    if x<0:
        x = -x
    return x

def bigger(x,y):
    if x<y:
        return y
    else:
        return x
# print bigger(4,2)

def biggest (x,y,z):
    if x>y and x>z:
        return x
    elif y>x and y>z:
        return y
    else:
         return z
#print biggest(6,2,3)
#print biggest(6,2,7)
#print biggest(6,9,3)

def print_numbers(x):
        y = 1
        while y<=x:
            print y
            y = y+1

def factorial(n):
    m = 1
    while n>0:
        m = m*n
        n = n-1
    return m

print factorial(52)
