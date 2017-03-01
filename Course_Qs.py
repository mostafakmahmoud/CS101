def remove_tags(string):
    #Function to remove html tags
    start = string.find('<')
    while start != -1:
        end = string.find('>', start)
        string = string[:start] + ' ' + string[end+1:]
        start = string.find('<')
    return string.split()

def date_converter(dictionary, string):
    #change date format from numbers to written
    month, day, year = string.split('/')
    date = day + ' ' + dictionary[int(month)] + ' ' + year
    return date

    english = {1:"January", 2:"February", 3:"March", 4:"April", 5:"May",
    6:"June", 7:"July", 8:"August", 9:"September",10:"October",
    11:"November", 12:"December"}

    swedish = {1:"januari", 2:"februari", 3:"mars", 4:"april", 5:"maj",
    6:"juni", 7:"juli", 8:"augusti", 9:"september",10:"oktober",
    11:"november", 12:"december"}

def longest_repetition(input_list):
    #takes as input a list, and returns
    #the element that has the has the most
    # consecutive repetitions.
    best_element = None
    length = 0
    current = None
    current_length = 0
    for element in input_list:
        if current != element:
            current = element
            current_length = 1
        else:
            current_length = current_length + 1
        if current_length > length:
            best_element = current
            length = current_length
    return best_element
