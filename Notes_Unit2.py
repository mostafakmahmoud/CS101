# HOW TO REPEAT
#PROCEDURES and CONTROL

#def <name>(<parameters>):
#    <BLOCK>

# if <TestExpression>
#   <BLOCK>

# while <TestExpression>:
#   <BLOCK>

#Example of function
def get_next_target (S):
    start_link = S.find('<a href=')
    start_quote = S.find('"', start_link)
    end_quote = S.find('"', start_quote+1)
    url = S [start_quote+1 : end_quote]
    return url, end_quote

#Example function to find the bigger of two numbers.
def bigger(x,y):
    if x<y:
        return y
    else:
        return x

# Example function to decide if a name begins with D,N, or Else
def is_friend (name):
    if name[0] == 'D' or name[0] == 'N':
        return True
    else:
        return False
