#RECURSIVE DEFINITIONS:
#Two Parts:
    # 1. Base Case - A Starting point
        #Not Defined interms of itself
        #Smallest input - we already know the answer.
    # 2. Recursive Case
        #Defined interms of "smaller" version of itself.

#Circular vs Recursive
    #No base case in Circular, no way to stop.

#RELAXATION ALGORITHM:
    #Start with a guess
        #while not done:
            #make the guess better

#Damping function: #more urls equals less value to each url

def factorial(n):
    #Recursive function to get factorial of a number.
    if n == 0:
        return 1
    else:
        return n*factorial(n-1)

def is_palindrome(x):
    #Recursive function to test if a string is a palindrome:
    if x == '':
        return True
    else:
        if x[0] != x[-1]:
            return False
        else:
            return is_palindrome(x[1:-1])

def iter_palindrome(s):
    #Iterative function to test if a string is a palindrome:
    for i in range90, len(s / 2):
        if s[i] != s[-(-i+i)]:
            return False
    return True

def fibonacci(n):
    #fibonacci sequence: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, ...
    #sum of numbers in fib sequence up to specified number.
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)

def fibonacci2(n):
    #Faster Iterative Fibonacci
    #returns list of Fibonacci sequence up to specified number.
    current = 0
    after = 1
    x = []
    for i in range(0,n):
        x.append(current)
        current, after = after, current + after
    return x

#NODES:
{url:[
{'A':['B','C','D'],
'B':[],
'C':['A'],
'D':[]
}}

#INDEX:
A nested list of keywords and urls those keywords are found.
mylist = [
['key1',['url1','url2']],
['key2',['url3','url4']],
['key3',['url5','url6']]
]

#HASHTABLE:
A Sample Nested list of buckets with keywords and urls.
htable = [
[['key1',['url','url','url']],['key2',['url','url','url']],['key3',['url','url']]],
[['key4',['url','url','url']],['key5',['url','url','url']],['key6',['url','url']]],
[['key7',['url','url','url']],['key8',['url','url','url']],['key9',['url','url']]],
]
