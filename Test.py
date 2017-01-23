def replace_spy(a):
    a[2] = a[2]+1
    return a
spy = [0,0,7]
print replace_spy(spy)
