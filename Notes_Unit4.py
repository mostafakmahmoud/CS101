#DATA STRUCTURES
#'string'.split()

mylist = [
['key1',['url1','url2']],
['key2',['url3','url4']],
['key3',['url5','url6']]
]

# Define a procedure, add_to_index,
    # that takes 3 inputs:
    # - an index: [[<keyword>,[<url>,...]],...]
    # - a keyword: String
    # - a url: String
    # If the keyword is already
    # in the index, add the url
    # to the list of urls associated
    # with that keyword.
    # If the keyword is not in the index,
    # add an entry to the index: [keyword,[url]]
index = []
def add_to_index(index, keyword, url):
    for entry in index:
        if entry[0] == keyword:
            entry[1].append(url)
            return
    index.append([keyword, [url]]
    #add_to_index(index,'udacity','http://udacity.com')
    #add_to_index(index,'computing','http://acm.org')
    #add_to_index(index,'udacity','http://npr.org')
    #print index
    #>>> [['udacity', ['http://udacity.com', 'http://npr.org']],
    #>>> ['computing', ['http://acm.org']]]

def lookup(index,keyword):
    for entry in index:
        if entry[0] == keyword:
            return entry[1]
    return []

def add_page_to_index(index,url,content):
    words = content.split()
    for word in words:
        add_to_index(index, word, url)

def add_to_index(index, keyword, url):
    #look if keyword is already in index, add url to list of urls.
    for entry in index:
        if entry[0] == keyword:
            entry[1].append(url)
            return
    #if not found, add new entry.
    index.append([keyword, [url]])

def lookup(index,keyword):
    for entry in index:
        if entry[0] == keyword:
            return entry[1]
    return []

def add_page_to_index(index,url,content):
    words = content.split()
    for word in words:
        add_to_index(index, word, url)

# The built-in <string>.split() procedure works
# okay, but fails to find all the words on a page
# because it only uses whitespace to split the
# string. To do better, we should also use punctuation
# marks to split the page into words.
# Define a procedure, split_string, that takes two
# inputs: the string to split and a string containing
# all of the characters considered separators. The
# procedure should return a list of strings that break
# the source string up by the characters in the
# splitlist.
def split_string(source,splitlist):
    output = []
    atsplit = True #At a split point
    for char in source: #iterate throuhg string by each Letter
        if char in splitlist:
            atsplit = True
        else:
            if atsplit:
                output.append(char)
                atsplit = False
            else:
                #add character to last word
                output[-1] = output[-1] + char
    return output
