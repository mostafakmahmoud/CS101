#Space to try out stuff
#q = [1,2,3,4,5,6]
#q =  [1, [2,3], 4, [5,6]]
q = [1, [2, 3, [4, [5, 6]]]]

final = []
i = len(q)-1
while i >= 0:
    final.append(q[i])
    i = i-1

print final

"""
if list:
    result = []
    x = len(p)
    while x >= 0:
        append p[x] to result
        x = x-1
return result
"""
