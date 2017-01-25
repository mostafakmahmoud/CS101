#NOTES:
    #STRUCTURED DATA
    #LISTS
    #DICTIONARIES
    #ALIASING
    #MUTATION
    #For <Name> in <List>:
        #   <Block>
    #LIST OPERATIONS:
        #APPEND (adds another value - mutates the list passed to it)
            #LIST.append(ELEMENT)

        #+ (concatnates lists - doesnt mutate the lists passed to it)
            #LIST + LIST

        #Len - (number of elements in the list)
            #len(LIST)

        #Index (finds position of element in a list)
            #LIST.index(ELEMENT)

        #in (finds if element is in list)
            #VALUE in LIST - returns Boolean True and False

        #pop (mutates the list by removing and returning its last element.)
            #LIST.pop()

#FIND ELEMENT:
    # Define a procedure, find_element,
    # that takes as its inputs a list
    # and a value of any type, and
    # returns the index of the first
    # element in the input list that
    # matches the value.
    # If there is no matching element,
    # return -1.
def find_element(p,x):
    position = 0
    for n in p:
        if x == n:
            return position
            break
        position = position + 1
    if position==len(p):
        return -1
    #print find_element([0,1,2,3,4,5,6,7],2)
    #print find_element(['alpha','beta'],'gamma')
def find_element2(p,x):
    if x in p:
        return p.index(x)
    else:
        return -1

# Define a procedure, union,
    # that takes as inputs two lists.
    # It should modify the first input
    # list to be the set union of the two
    # lists. You may assume the first list
    # is a set, that is, it contains no
    # repeated elements.
def union(a,b):
    for i in b:
        if i not in a:
            a.append(i)
    return a

#Measure how Udacious names in a list are (starting with U):
def measure_udacity(p):
    x=0
    for n in p:
        if n[0] == 'U':
            x = x+1
    return x
