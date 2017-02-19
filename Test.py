#Recursive function to get factorial of a number.
def factorial(n):
    if n == 0:
        return 1
    else:
        return n*factorial(n-1)

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

# fibonacci sequence: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, ...
def fibonacci(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)
#print fibonacci(3)
# Finished in 7.727 seconds

def fibonacci2(n):
    current = 0
    after = 1
    x = []
    for i in range(0,n):
        x.append(current)
        current, after = after, current + after
    return x

def golden_ratio(x):
    my_list = fibonacci2(x)
    g_ratio = []
    for i in my_list:
        g_ratio.append(my_list[i+1]/my_list[i])
    return g_ratio

# print fibonacci2(36)
print golden_ratio(36)
