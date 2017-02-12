def test_hash_function(func, keys, size):
    results = [0] * size
    keys_used = []
    for w in keys:
        if w not in keys_used:
            hv = func(w, size)
            results[hv]+1
            keys_used.append(w)
    return results

def hashtable_lookup(htable, key):
    bucket = hashtable_get_bucket(htable, key)
    for entry in bucket:
        if entry[0] == key:
            return entry[1]
    return None

def hashtable_update(htable, key, value):
    bucket = hashtable_get_bucket(htable, key)
    for entry in bucket:
        if entry[0] == key:
            entry[1] = value
            return
    bucket.append([key,value])
    return

def hashtable_get_bucket(htable, key):
    return htable[hash_string(key, len(htable))]

def hash_string(keyword, buckets):
    total = 0
    for letter in keyword:
        total = total + ord(letter)
    return total%buckets

def make_hashtable(nbuckets):
    table = []
    for i in range(0, nbuckets):
        table.append([])
    return table

def hashtable_add(htable,key,value):
    #gets the position and appends the word at that position.
    position = hash_string(key,len(htable))
    htable[position].append([key,value])
    return htable
    #gets bucket then appends the word to it.
    ##hasthable_get_bucket(htable, key).append([key, value])

table = [[['Ellis', 11], ['Francis', 13]], [], [['Bill', 17], ['Zoe', 14]],
[['Coach', 4]], [['Louis', 29], ['Nick', 2], ['Rochelle', 4]]]

hashtable_update(table, 'Bill', 42)
hashtable_update(table, 'Rochelle', 94)
hashtable_update(table, 'Zed', 68)
print table
#>>> [[['Ellis', 11], ['Francis', 13]], [['Zed', 68]], [['Bill', 42],
#>>> ['Zoe', 14]], [['Coach', 4]], [['Louis', 29], ['Nick', 2],
#>>> ['Rochelle', 94]]]
