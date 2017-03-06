arc#Space to try out stuff
#string = "John is connected to Bryant, Debra, Walter.\
#John likes to play The Movie: The Game, The Legend of Corgi, Dinosaur Diner."

Data = {'John': {'Friends':['Bryant', 'Debra', 'Walter'],
'Plays': ['The Game', 'The Legend of Corgi', 'Dinosaur Diner']}}

string="John is connected to Bryant, Debra, Walter.\
    John likes to play The Movie: The Game, The Legend of Corgi, Dinosaur Diner.\
    Bryant is connected to Olive, Ollie, Freda, Mercedes.\
    Bryant likes to play City Comptroller: The Fiscal Dilemma, Super Mushroom Man.\
    Mercedes is connected to Walter, Robin, Bryant.\
    Mercedes likes to play The Legend of Corgi, Pirates in Java Island, Seahorse Adventures.\
"
"   Olive is connected to John, Ollie.\
    Olive likes to play The Legend of Corgi, Starfleet Commander.\
    Debra is connected to Walter, Levi, Jennie, Robin.\
    Debra likes to play Seven Schemers, Pirates in Java Island, Dwarves and Swords.\
    Walter is connected to John, Levi, Bryant.\
    Walter likes to play Seahorse Adventures, Ninja Hamsters, Super Mushroom Man.\
    Levi is connected to Ollie, John, Walter.\
    Levi likes to play The Legend of Corgi, Seven Schemers, City Comptroller: The Fiscal Dilemma.\
    Ollie is connected to Mercedes, Freda, Bryant.\
    Ollie likes to play Call of Arms, Dwarves and Swords, The Movie: The Game.\
    Jennie is connected to Levi, John, Freda, Robin.\
    Jennie likes to play Super Mushroom Man, Dinosaur Diner, Call of Arms.\
    Robin is connected to Ollie.\
    Robin likes to play Call of Arms, Dwarves and Swords.\
    Freda is connected to Olive, John, Debra.\
    Freda likes to play Starfleet Commander, Ninja Hamsters, Seahorse Adventures."

"""
John
['Bryant', 'Debra', 'Walter']
['The Movie: The Game', 'The Legend of Corgi', 'Dinosaur Diner']
"""

#def create_data_structure(string_input):
#    network = {}
#    added_names = []
#    return network

added_names = []
network = {}

while len(string) > 10:
    name = string[0:string.find(" ")]
    print name           #Get Subject Name
    if name not in added_names:                  #Check if already in added_names
        added_names.append(name)                 #If not, add to added_names
        network[name]={'Friends':[], 'Plays':[]} #Create an entry for the name

        Friends = string[string.find('to')+3: string.find('.')].split(', ') #Get Friends
        network[name]['Friends'] = Friends    #Add friends under subject name

        Plays = string[string.find('play')+5:string.find('.',string.find('play'))].split(', ') #Get Plays
        network[name]['Plays'] = Plays

        string = string[string.find('.',string.find('play'))+1:]
        print string
print network

#dictt = {}
#dictt['name']={'Friends':[], 'Plays':[]}
#dictt['name']['Friends'].append('test string')
#print dictt
