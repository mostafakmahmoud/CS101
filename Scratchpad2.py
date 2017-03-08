#Space to try out stuff

data_structure = {'Freda': {'Plays': ['Starfleet Commander', 'Ninja Hamsters', 'Seahorse Adventures'], 'Friends': ['Olive', 'John', 'Debra']},
 'Ali': {'Plays': ['Ghost Recon', 'Battlefield', 'TitanFall2'], 'Friends': []},
 'Ollie': {'Plays': ['Call of Arms', 'Dwarves and Swords', 'The Movie: The Game'], 'Friends': ['Mercedes', 'Freda', 'Bryant']},
 'Debra': {'Plays': ['Seven Schemers', 'Pirates in Java Island', 'Dwarves and Swords'], 'Friends': ['Walter', 'Levi', 'Jennie', 'Robin']},
 'Olive': {'Plays': ['The Legend of Corgi', 'Starfleet Commander'], 'Friends': ['John', 'Ollie']},
 'Levi': {'Plays': ['The Legend of Corgi', 'Seven Schemers', 'City Comptroller: The Fiscal Dilemma'], 'Friends': ['Ollie', 'John', 'Walter']},
 'Jennie': {'Plays': ['Super Mushroom Man', 'Dinosaur Diner', 'Call of Arms'], 'Friends': ['Levi', 'John', 'Freda', 'Robin']},
 'Mercedes': {'Plays': ['The Legend of Corgi', 'Pirates in Java Island', 'Seahorse Adventures'], 'Friends': ['Walter', 'Robin', 'Bryant']},
 'John': {'Plays': ['The Movie: The Game', 'The Legend of Corgi', 'Dinosaur Diner'], 'Friends': ['Bryant', 'Debra', 'Walter']},
 'Robin': {'Plays': ['Call of Arms', 'Dwarves and Swords'], 'Friends': ['Ollie']},
 'Bryant': {'Plays': ['City Comptroller: The Fiscal Dilemma', 'Super Mushroom Man'], 'Friends': ['Olive', 'Ollie', 'Freda', 'Mercedes']},
 'Walter': {'Plays': ['Seahorse Adventures', 'Ninja Hamsters', 'Super Mushroom Man'], 'Friends': ['John', 'Levi', 'Bryant']}}

string="John is connected to Bryant, Debra, Walter.\
John likes to play The Movie: The Game, The Legend of Corgi, Dinosaur Diner.\
Bryant is connected to Olive, Ollie, Freda, Mercedes.\
Bryant likes to play City Comptroller: The Fiscal Dilemma, Super Mushroom Man.\
Mercedes is connected to Walter, Robin, Bryant.\
Mercedes likes to play The Legend of Corgi, Pirates in Java Island, Seahorse Adventures.\
Olive is connected to John, Ollie.\
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
Freda likes to play Starfleet Commander, Ninja Hamsters, Seahorse Adventures.\
Ali likes to play Ghost Recon, Battlefield, TitanFall2."

def create_data_structure(string):
    #Parses a block of text and stores relevant information into a data structure.
    #Returns the data structure (network)

    added_names = []
    network = {}

    while len(string) > 1:
        name = string[0:string.find(" ")]            #Get Subject Name
        #print name                                  #uncomment for testing
        if name not in added_names:                  #Check if already in added_names
            added_names.append(name)                 #If not, add to added_names
            network[name]={'Friends':[], 'Plays':[]} #Create an entry for the name

        if string.find('connected to') != -1:        #Checks if the user has any connections
            Friends = string[string.find('connected to')+13: string.find('.')].split(', ') #Get Friends text and split by ,
            network[name]['Friends'] = Friends       #Add friends under subject name
        else:
            network[name]['Friends'] = []            #Add an empty list if there are no connections.
        #print network[name]['Friends']              #uncomment for testing

        if string.find('play') != -1:                #Checks if the users plays any games.
            Plays = string[string.find('play')+5:string.find('.',string.find('play'))].split(', ') #Get Plays text and split by ,
            network[name]['Plays'] = Plays           #Add plays under subject name
        else:
            network[name]['Plays'] = []              #Add an empty list if there are no games.
        #print network[name]['Plays']                #uncomment for testing

        string = string[string.find('.',string.find('play'))+1:] #reassign string minus last user.

    return network

def get_connections(network, user):
    if user in network:
        return network[user]['Friends']
    else:
        return None

def get_games_liked(network,user):
    if user in network:
        return network[user]['Plays']
    else:
        return None

def add_connection(network, user_A, user_B):
    if user_A not in network or user_B not in network:
        return False
    elif user_B in network[user_A]['Friends']:
        return network
    else:
        network[user_A]['Friends'].append(user_B)
        return network

def add_new_user(network, user, games):
    if user in network:
        return network
    else:
        network[user]={'Friends':[], 'Plays':games}
        return network

def get_secondary_connections(network, user):
    #Finds all the secondary connections (i.e. connections of connections) of a
    #given user.
    #removes duplicate values.
    sec_conn = []                               #results list
    if user not in network:
        return None
    elif network[user]['Friends'] == []:        #checks if user has friends
        return network[user]['Friends']
    else:
        for each in network[user]['Friends']:           #for each connection in primary friends:
            for sec_each in network[each]['Friends']:   #for each of their connections
                if sec_each not in sec_conn:            #if not already added to sec_conn
                    sec_conn.append(sec_each)           #add it
    return sec_conn

def count_common_connections(network, user_A, user_B):
    #Finds the number of people that user_A and user_B have in common.
    count = 0
    user_A_conn = network[user_A]['Friends']    #gets user_A Friends
    user_B_conn = network[user_B]['Friends']    #gets user_B Friends
    for each in user_A_conn:                    #for each friend:
        if each in user_B_conn:                 #if in B list:
            count = count + 1                   #increase the count by 1
    return count

network = create_data_structure(string)
#print network
print network['Mercedes']['Friends']
print network['John']['Friends']
print count_common_connections(network, "Mercedes", "John")
