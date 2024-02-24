#v.1.6.7
import socket
import threading
import random
from datetime import datetime
from game import Game
import village as v
import configurations as config
'---------------------------------------------------CONNECTION--------------------------------------------------------'

#Create a server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Bind the socket to a specific IP and Port
server_ip = '0.0.0.0'
server_port = 5555
server_socket.bind((server_ip, server_port))

#Listen for incoming connections
server_socket.listen(5)
print(f"Server listening on {server_ip}:{server_port}")

'---------------------------------------------------DATA--------------------------------------------------------'
#Send data to client
def send(conn, data):
    try:
        # Send a message to the client
        conn.send(data.encode())
    except socket.error as e:
        print(e)
        return 'error'  
#Read data from the client
def read(conn):
    try:
        # Receive the message from the client
        return conn.recv(1024).decode()
    except socket.error as e:
        print(e)
        return 'error'
#Send a datapack to the client
    

def send_data(conn, data):
    try:
        data_pack = ','.join(map(str, data))
        conn.send(data_pack.encode())
    except socket.error as e:
        print(e)
        return 'error'

def send_data_state(conn, state, data):
    try:
        conn.send(str(state).encode())
        print(read(conn))

        data_pack = ','.join(map(str, data))
        conn.send(data_pack.encode())
    except socket.error as e:
        print(e)
        return 'error'
    
#def send_data(conn, data, state):
#    try:
#        data_state = add_state(data, state)
#        #pack the data
#        data_pack = ','.join(map(str, data_state))
#        # Send a message to the client
#        conn.send(data_pack.encode())
#        return read(conn)   #read the return
#    except socket.error as e:
#        print(e)
#        return 'error'

#Add a state var to the data
def add_state(data, state):
    data = data + (state,)
    return data

'---------------------------------------------------DATABASE--------------------------------------------------------'
#Create a dictionary used as database
user_database = {}

#Save the database in a file
def save_database(database, filename='user_database.txt'):
    try:
        with open(filename, 'w') as file:   #Open the file
            for u, data in database.items():
                p, x, y, lt, w, c, i, p1, p2, pt, hq, tc, cp, im, f, wh = data
                file.write(f'{u},{p},{x},{y},{lt},{w},{c},{i},{p1},{p2},{pt},{hq},{tc},{cp},{im},{f},{wh}\n')    #write the values
        print('database saved.')
                
    except FileNotFoundError:
        print('database fail to save, file not found.')

#Load the database from a file
def load_database(filename='user_database.txt'):
    database = {}   #Create an empty dictionary
    try:
        with open (filename, 'r') as file:  #open the file
            for line in file:
                u, p, x, y, lt, w, c, i, p1, p2, pt, hq, tc, cp, im, f, wh = line.strip().split(',')  #Read a line and split the values
                database[u] = [p, x, y, lt, w, c, i, p1, p2, pt, hq, tc, cp, im, f, wh]               #save the values in the dictionary
        print('database loaded.')
           
    except FileNotFoundError:
        print('database fail to load, file not found.')

    return database

def new_random_cords():
    x = random.randint(0, config.map_width-1)
    y = random.randint(0,config.map_height-1)
    return x, y


#Add a new user to database dictionary
def add_new_user(database, username, password):
    x, y = new_random_cords()
    #'USERNAME': ['PASSWORD', X, Y, LOGOUT_DATATIME, WOOD, CLAY, IRON, PROGRESS, PROGRESS2, PROGRESS_TIME, HEADQUARTES, TIMBERCAMP, CLAYPIT, IRONMINE, FARM, WAREHOUSE]
    database[username] = [password, x, y, str(datetime.now()), 500, 500, 500, -1, -1, str(datetime.now()), v.village[0].min_lv, v.village[1].min_lv, v.village[2].min_lv, v.village[3].min_lv, v.village[4].min_lv, v.village[5].min_lv]
    save_database(database)

#Load the user data from the dictionary database
def load_user_data(database, username):
    #x = database[username][1]                   # X Cord
    #y = database[username][2]                   # Y Cord
    logout_time = datetime.strptime((database[username][3]), "%Y-%m-%d %H:%M:%S.%f")       #LOGOUT TIME    
    w = float(database[username][4])            #WOOD
    c = float(database[username][5])            #CLAY
    i = float(database[username][6])            #IRON
    p1 = database[username][7]                  #PROGRESS1
    p2 = database[username][8]                  #PROGRESS2
    pt = datetime.strptime((database[username][9]), "%Y-%m-%d %H:%M:%S.%f")                  #PROGRESS TIME
    hq = database[username][10]                  #HEADQUARTES
    tc = database[username][11]                  #TIMBER CAMP
    cp = database[username][12]                  #CLAY PIT
    im = database[username][13]                 #ITON MINE
    f = database[username][14]                  #FARM
    wh = database[username][15]                 #WAREHOUSE 
    data = logout_time, w, c, i, p1, p2, pt, hq, tc, cp, im, f, wh     #pack the data in a tuple
    return data

#save the data in the dictionary database
def update_user_data(database, username, current_time, data):
    w, c, i, p1, p2, pt, hq, tc, cp, im, f, wh = data       #unpack the data
    #database[username][1] = x
    #database[username][2] = y
    database[username][3] = current_time
    database[username][4] = w
    database[username][5] = c
    database[username][6] = i
    database[username][7] = p1
    database[username][8] = p2
    database[username][9] = pt
    database[username][10] = hq
    database[username][11] = tc
    database[username][12] = cp
    database[username][13] = im
    database[username][14] = f
    database[username][15] = wh

def pack_user_cords(database):
    data = []
    for user in database:
        data.append(user)
        data.append(database[user][1])
        data.append(database[user][2])
    return data

#Autosave timer
#def autosave(_time):
#    if datetime.now() > _time + start_autosave:
#        start_autosave = datetime.now()
#        return True
#save_database(user_database)
'---------------------------------------------------GAMEPLAY--------------------------------------------------------'
def play(user_database, username):
    print('play')
    send(conn, str(config.game_speed))  

    g = Game(load_user_data(user_database, username), config.game_speed)
    playing = True
    state = 0
    while playing:
        current_time = datetime.now()
        client_action = read(conn)
        print(client_action)
        
        if client_action == 'error' or client_action == 'logout':    #lost connection
            playing = False
            #break
            #pass

        elif client_action == 'upgrade':     #send game data
            send(conn, 'index')
            upgrade_index = int(read(conn))
            if g.upgrade_avaliable(upgrade_index, g.village_level[upgrade_index]):      #if can upgrade
                g.add_to_progress(upgrade_index) 
            
        elif client_action == 'main':     #send game data  
            g.progress_countdown() 

            if g.delay(1):                                                                  #after a X time execute production
                g.production(1)
            
            update_user_data(user_database, username, current_time, g.get_data())

            game_data = g.get_data()
            send_data(conn, game_data)


        elif client_action == 'map_cords':     #send game data
            data = pack_user_cords(user_database)
            send_data(conn, (data))

        elif client_action == 'map':     #send game data
            send_data(conn, (current_time, username))

        else:                           #send something else
            send(conn, 'UNKNOWN!!')

    save_database(user_database)


'---------------------------------------------------CLIENT--------------------------------------------------------'



#Client Thread
def client_conn(conn, addr):
    print('Connected to: ', addr)
    user_database = load_database()     #Load the database from the file
    print(user_database)

    send(conn, 'connection')             #send a msg to connected client
    connected = True
    while connected:
        choice = read(conn)            #read the msg from the connectd client
        print(f'choise:{choice}')

        if choice == 'login':
            print(choice)
            send(conn, 'username')      #ask for username and password
            username = read(conn)
            send(conn, 'password')
            password = read(conn)

            #if the username exists and the password match
            if username in user_database and user_database[username][0] == password:
                send(conn, 'connected')

                play(user_database, username)
                send(conn, 'loggedout')
            else:
                send(conn, 'fail')

        elif choice == 'register':
            print(choice)

            send(conn, 'username')                                                                  #ask for username and password and confirm password
            username = read(conn)
            send(conn, 'password')
            password = read(conn)
            send(conn, 'password2')
            password2 = read(conn)

            print(username, password, password2)

            if username in user_database:                                                           #if username already exists
                send(conn, 'exists')
            elif password != password2:                                                             #if password dont match
                send(conn, 'incorrect')
            else:                                                                                   #add the username and password to dictionary database
                send(conn, 'created')
                add_new_user(user_database, username, password)


        else:   #disconnect
            connected = False


    
    print(f'Connection closed with: {addr}')
    conn.close()


'-----------------------------------------------------------------------------------------------------------'
while True:                                
    conn, addr = server_socket.accept()     # Wait for a connection   

    # Create a new thread to handle the client
    conn_client = threading.Thread(target=client_conn, args=(conn, addr))
    conn_client.start() #start the thread
