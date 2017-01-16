## STRING METHODS:
len(string) #Length of String
string.lower() #Convert to Lowercase
string.upper() #Convert to Uppercase
str(variable) #Convert non-strings to strings

## STRING FORMATTING WITH %:
string_1 = "Camelot"
string_2 = "place"
print "Let's not go to %s. It's a silly %s." % (string_1, string_2)
Let's not go to Camelot.  It's a silly place.

## INDEXING STRINGS:
'string goes here' [0]
     # 's'
'string goes here' [1+1]
     # 'r'
'string goes here' [-1]
     # 'e' #negative index means start counting back from the end of string.
'string goes here' [1:5]
     # 'trin' #select from string from [1] up to but not including [5]
'string goes here' [1:]
     # 'tring goes here'

## FINDING STRINGS:
'string'.find('string')
#Number that gives first position in search string where the target string appears
#If not found, return -1

'This is a string'.find('string' ,5)
#finds target string starting from stated position
