def make_hashtable(nbuckets):
    table = []
    for i in range(0, nbuckets):
        table.append([])
    return table

print make_hashtable(3)
