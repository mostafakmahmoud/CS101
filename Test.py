def test_hash_function(func, keys, size):
    results = [0] * size
    keys_used = []
    for w in keys:
        if w not in keys_used:
            hv = func(w, size)
            results[hv]+1
            keys_used.append(w)
    return results

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

def hashtable_lookup(htable, key):
    bucket = hashtable_get_bucket(htable, key)
    for entry in bucket:
        if key in entry:
            return entry[1]
    return None


table = [
[['Ellis', 11], ['Francis', 13]]
, [],
[['Bill', 17], ['Zoe', 14]],
[['Coach', 4]],
[['Louis', 29], ['Nick', 2], ['Rochelle', 4]]]

print hashtable_lookup(table, 'Francis')
#>>> 13

print hashtable_lookup(table, 'Louis')
#>>> 29

print hashtable_lookup(table, 'Zoe')
#>>> 14

print hashtable_lookup(table, 'jjj')
