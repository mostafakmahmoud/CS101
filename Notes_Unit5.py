eval(code) #evaluating the string of code passed to it:
#Hash Table - DICTIONARIES
range(start,stop) #outputs list of numbers from start to stop-1
ord(<one-letter-string>) #converts a character into a number.
chr(<number>) #converts a number to its corresponding string.
chr(ord(A)) == A  #They are inverses.
#Mapping ord function:
alphabet = [97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122]
cap = [65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90]

#DICTIONARIES:
elements = {'hydrogen':1, 'helium':2, 'carbon':6}
elements['oxygen'] = 8 #adds element to dictionary
'carbon' in elements  #True or False
elements['oxygen'] = [1,2,3,4] #value can be anything
elements2 = {}
elements2['H'] = {'name': 'Hydrogen', 'number':1, 'weight': 1.00794}

#Some functions created during Unit 5:

#function to measure how long it takes to execute something.
def time_execution(code):
    import time
    start = time.clock()
    result = eval(code)
    run_time = time.clock() - start
    return result, run_time
## whatever function you wanna measure:
def spin_loop(n):
    i = 0
    while i < n:
        i = i+1
##testing statment
print time_execution('spin_loop(10 ** 9)')[1]
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

# Dictionaries of Dictionaries (of Dictionaries)

# The next several questions concern the data structure below for keeping
# track of Udacity's courses (where all of the values are strings):

courses = {
    'feb2012': { 'cs101': {'name': 'Building a Search Engine',
                           'teacher': 'Dave',
                           'assistant': 'Peter C.'},
                 'cs373': {'name': 'Programming a Robotic Car',
                           'teacher': 'Sebastian',
                           'assistant': 'Andy'}},
    'apr2012': { 'cs101': {'name': 'Building a Search Engine',
                           'teacher': 'Dave',
                           'assistant': 'Sarah'},
                 'cs212': {'name': 'The Design of Computer Programs',
                           'teacher': 'Peter N.',
                           'assistant': 'Andy',
                           'prereq': 'cs101'},
                 'cs253':
                {'name': 'Web Application Engineering - Building a Blog',
                           'teacher': 'Steve',
                           'prereq': 'cs101'},
                 'cs262':
                {'name': 'Programming Languages - Building a Web Browser',
                           'teacher': 'Wes',
                           'assistant': 'Peter C.',
                           'prereq': 'cs101'},
                 'cs373': {'name': 'Programming a Robotic Car',
                           'teacher': 'Sebastian'},
                 'cs387': {'name': 'Applied Cryptography',
                           'teacher': 'Dave'}},
    'jan2044': { 'cs001': {'name': 'Building a Quantum Holodeck',
                           'teacher': 'Dorina'},
                 'cs003': {'name': 'Programming a Robotic Robotics Teacher',
                           'teacher': 'Jasper'},
                     }
    }

def courses_offered(courses, hexamester):
    res = []
    for c in courses[hexamester]:
        res.append(c)
    return res

def when_offered(courses,course):
    offered = []
    for c in courses:
        if course in courses[c]:
            offered.append(c)
    return offered

def is_offered(courses, course, hexamester):
    if course in courses[hexamester]:
        return True
    else:
        return False

def involved(courses, person):
    result = {}
    mylist = []
    for semester in courses:
        for course in courses[semester]:
            for i in courses[semester][course]:
                if courses[semester][course][i] == person:
                    mylist.append(course)
                    result[semester] = mylist
        mylist = []
    return result

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
#print htable[0] #bucket
#print htable[0][1] #entry
#print htable [0][1][0] #key
#print htable [0][1][1] #urls
#print 'key' in htable [0][1][0]
