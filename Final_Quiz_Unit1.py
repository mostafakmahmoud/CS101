# Write Python code that assigns to the
# variable url a string that is the value
# of the first URL that appears in a link
# tag in the string page.
# Your code should print http://udacity.com
# page = contents of a web page

page = '<a href="http://udacity.com">Hello world</a>'
page2 = ('<div id="top_bin"><div id="top_content" class="width960">'
'<div class="udacity float-left"><a href="http://udacity.com">')
start_link = page.find('<a href=')

#MY SOLUTION:

target = '<a href=' # Begining of string
ending = '.com"'    # Ending of string
start = page.find(target) + 9 #Start Point
end = page.find(ending) + 4 #End Point

url = page[start:end]
print url
