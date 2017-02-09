alphabet = [97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108,
 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122]

cap = [65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80,
 81, 82, 83, 84, 85, 86, 87, 88, 89, 90]

#sample nested list
mylist = [
['key1',['url1','url2']],
['key2',['url3','url4']],
['key3',['url5','url6']]
]

htable = [
[['key1',['url','url','url']],['key2',['url','url','url']],['key3',['url','url']]],
[['key4',['url','url','url']],['key5',['url','url','url']],['key6',['url','url']]],
[['key7',['url','url','url']],['key8',['url','url','url']],['key9',['url','url']]],
]

print htable[0] #bucket
print htable[0][1] #entry
print htable [0][1][0] #key
print htable [0][1][1] #urls
print 'key' in htable [0][1][0]
