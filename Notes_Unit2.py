# HOW TO REPEAT
#PROCEDURES and CONTROL
#def - while - if

#Function to find the bigger of two numbers:
def bigger(x,y):
    if x<y:
        return y
    else:
        return x

#Function to find the smaller of two numbers:
def smaller(a,b):
    if a < b:
        return a
    else:
        return b

#Function to find the biggest of three numbers:
def biggest (a,b,c):
    return bigger(a,bigger(b,c))

#Functions to get the Median from three numbers:
def median1(x,y,z):
    q = bigger(x,y)
    w = bigger(y,z)
    e = smaller(q,w)

    if e>x and e>z:
        return bigger(x,z)
    else:
        return e

def median2(a,b,c):
    big = biggest(a,b,c)
    if big == a:
        return bigger(b,c)
    if big == b:
        return bigger(a,c)
    else:
        return bigger(a,b)

# Example function to decide if a name begins with D,N, or Else
def is_friend (name):
    if name[0] == 'D' or name[0] == 'N':
        return True
    else:
        return False
