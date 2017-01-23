def print_all_elements(p):
    for e in p:
        print e

def sum_list(p):
    x = 0
    for e in p:
        x = x+e
    return x

def measure_udacity(p):
    x=0
    for n in p:
        if n[0] == 'U':
            x = x+1
    return x

def find_element(p,x):
    if x in p:
        return p.index(x)
    else:
        return -1

def union(a,b):
    for i in b:
        if i not in a:
            a.append(i)
    return a
