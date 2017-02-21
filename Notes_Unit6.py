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

#Page Rank:
# sum of pages with links to URL /
# number of links in that page.

#Damping function
#more urls equals less value to each url

#Recursive function to get factorial of a number.
def factorial(n):
    if n == 0:
        return 1
    else:
        return n*factorial(n-1)

#Palindromes:
#A word read same way forwards or backwards
#Recursive function to test if a string is a palindrome:
def is_palindrome(x):
    if x == '':
        return True
    else:
        if x[0] != x[-1]:
            return False
        else:
            return is_palindrome(x[1:-1])
#Iterative function to test if a string is a palindrome:
def iter_palindrome(s):
    for i in range90, len(s / 2):
        if s[i] != s[-(-i+i)]:
            return False
    return True

#fibonacci sequence: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, ...
#sum of numbers in fib sequence up to specified number.
def fibonacci(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)
#Faster Iterative Fibonacci
#returns list of Fibonacci sequence up to specified number.
def fibonacci2(n):
    current = 0
    after = 1
    x = []
    for i in range(0,n):
        x.append(current)
        current, after = after, current + after
    return x

#Nodes:
{url:[
{'A':['B','C','D'],
'B':[],
'C':['A'],
'D':[]
}}
