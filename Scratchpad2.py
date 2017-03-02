#Space to try out stuff

# Function to work out values required to sum to the pattern number

# Function to update pattern values based on calculation.
# calls calculation function
# pattern_dictionary = {1:0, 2:0, 4:0, 8:0, 16:0, 32:0, 64:0, 128:0}
# if 0 then .
# if 1 then x

# Function cellular_automaton:
# gets updated pattern_dictionary
# starts with the input_string
# loops for the number of generations

# Rules:
#          pattern in         position k in        contribution to
# Value    current string     new string           pattern number
#                                                  is 0 if replaced by '.'
#                                                  and value if replaced
#                                                  by 'x'
#   1       '...'               '.'                        1 * 0
#   2       '..x'               'x'                        2 * 1
#   4       '.x.'               'x'                        4 * 1
#   8       '.xx'               'x'                        8 * 1
#  16       'x..'               '.'                       16 * 0
#  32       'x.x'               '.'                       32 * 0
#  64       'xx.'               '.'                       64 * 0
# 128       'xxx'               'x'                      128 * 1
#                                                      ----------
#                                                           142

# Function to work out values required to sum to the pattern number
print 249%128
