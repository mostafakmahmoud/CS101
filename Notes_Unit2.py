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

# Example function to decide if a name begins with D,N, or Else:
def is_friend (name):
    if name[0] == 'D' or name[0] == 'N':
        return True
    else:
        return False

#Function to find last occurance of a string in a test:
def find_last(text, target):
    last_pos = text.find(target)
    if last_pos == -1:
        return last_pos
    else:
        while last_pos != -1:
                a = last_pos
                last_pos = text.find(target, last_pos+1)
        return a

#Function fix_machine - Superhero:
# Write a Python procedure fix_machine to take 2 string inputs
# and returns the 2nd input string as the output if all of its
# characters can be found in the 1st input string and "Give me
# something that's not useless next time." if it's impossible.
# Letters that are present in the 1st input string may be used
# as many times as necessary to create the 2nd string (you
# don't need to keep track of repeat usage).
# Bonus: Solve in 1 line
def fix_machine(debris, product):
    a = 0
    x = debris.find(product[a])
    if x != -1:
        while a<len(product) and x!=-1:
            x = debris.find(product[a])
            a = a+1
            if x == -1:
                return "Give me something that's not useless next time."
                break
        return product
    else:
        return "Give me something that's not useless next time."
    ### TEST CASES ###
    print "Test case 1: ", fix_machine('UdaciousUdacitee', 'Udacity')  #"Give me something that's not useless next time."
    print "Test case 2: ", fix_machine('buy me dat Unicorn', 'Udacity') #'Udacity'
    print "Test case 3: ", fix_machine('AEIOU and sometimes y... c', 'Udacity') # 'Udacity'
    print "Test case 4: ", fix_machine('wsx0-=mttrhix', 't-shirt') # 't-shirt'

#Function JUNGLE!:
# By AnnaGajdova from forums
# You are in the middle of a jungle.
# Suddenly you see an animal coming to you.
# Here is what you should do if the animal is:
# zebra >> "Try to ride a zebra!"
# cheetah >> If you are faster than a cheetah: "Run!"
#            If you are not: "Stay calm and wait!".
#            The speed of a cheetah is 115 km/h.
# anything else >> "Introduce yourself!"
# Define a procedure, jungle_animal,
# that takes as input a string and a number,
# an animal and your speed (in km/h),
# and prints out what to do.
def jungle_animal(animal, my_speed):
    if animal == 'zebra':
        return "Try to ride a zebra!"
    elif animal == 'cheetah':
        if my_speed > 115:
            return "Run!"
        else:
            return "Stay calm and wait!"
    else:
        return "Introduce yourself!"
    #print jungle_animal('cheetah', 30)
    #>>> "Stay calm and wait!"
    #print jungle_animal('gorilla', 21)
    #>>> "Introduce yourself!"

#Function LEAP_YEAR_BABY:
# By Ashwath from forums
# A leap year baby is a baby born on Feb 29, which occurs only on a leap year.
# Define a procedure is_leap_baby that takes 3 inputs: day, month and year
# and returns True if the date is a leap day (Feb 29 in a valid leap year)
# and False otherwise.
# A year that is a multiple of 4 is a leap year unless the year is
# divisible by 100 but not a multiple of 400 (so, 1900 is not a leap
# year but 2000 and 2004 are).
def is_leap_baby(day,month,year):
    # Write your code after this line.
    if year%4 == 0:
        if year%100 != 0 or year%400 == 0:
            if month == 2 and day == 29:
                return True
            else: return False
        else: return False
    else:
        return False

    # The function 'output' prints one of two statements based on whether
    # the is_leap_baby function returned True or False.

    def output(status,name):
        if status:
            print "%s is one of an extremely rare species. He is a leap year baby!" % name
        else:
            print "There's nothing special about %s's birthday. He is not a leap year baby!" % name

    # Test Cases

    output(is_leap_baby(29, 2, 1996), 'Calvin')
    #>>>Calvin is one of an extremely rare species. He is a leap year baby!

    output(is_leap_baby(19, 6, 1978), 'Garfield')
    #>>>There's nothing special about Garfield's birthday. He is not a leap year baby!

    output(is_leap_baby(29, 2, 2000), 'Hobbes')
    #>>>Hobbes is one of an extremely rare species. He is a leap year baby!

    output(is_leap_baby(29, 2, 1900), 'Charlie Brown')
    #>>>There's nothing special about Charlie Brown's birthday. He is not a leap year baby!

    output(is_leap_baby(28, 2, 1976), 'Odie')
    #>>>There's nothing special about Odie's birthday. He is not a leap year baby!
