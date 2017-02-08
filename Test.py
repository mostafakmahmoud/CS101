#sample nested list
mylist = [
['key1',['url1','url2']],
['key2',['url3','url4']],
['key3',['url5','url6']]
]

alphabet = [97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108,
 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122]

cap = [65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80,
 81, 82, 83, 84, 85, 86, 87, 88, 89, 90]

def make_hashtable(nbuckets):
    hashtable = []
    i = 0
    while i < nbuckets:
        hashtable.append([])
        i += 1
    return hashtable
print make_hashtable(5)

def test_hash_function(func, keys, size):
    results = [0] * size
    keys_used = []
    for w in keys:
        if w not in keys_used:
            hv = func(w, size)
            results[hv]+1
            keys_used.append(w)
    return results

def bad_hash_string(keyword, buckets):
    return ord(keyword[0]%buckets)

def hash_string(keyword, buckets):
    total = 0
    for letter in keyword:
        total = total + ord(letter)
    return total%buckets
