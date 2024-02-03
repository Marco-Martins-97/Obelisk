#v.1.6.1
import socket
import threading
from datetime import datetime
from game import Game
import village as v
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
#Read data from the client
def read(conn):
    try:
        # Receive the message from the client
        return conn.recv(1024).decode()
    except socket.error as e:
            print(e)
#Send a datapack to the client
def send_data(conn, data, state):
    try:
        data_state = add_state(data, state)
        #pack the data
        data_pack = ','.join(map(str, data_state))
        # Send a message to the client
        conn.send(data_pack.encode())
        return read(conn)   #read the return
    except socket.error as e:
            print(e)

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
                p, lt, w, c, i, p1, p2, pt, hq, tc, cp, im, f, wh = data
                file.write(f'{u},{p},{lt},{w},{c},{i},{p1},{p2},{pt},{hq},{tc},{cp},{im},{f},{wh}\n')    #write the values
                
    except FileNotFoundError:
        pass
    print('database saved.')

#Load the database from a file
def load_database(filename='user_database.txt'):
    database = {}   #Create an empty dictionary
    try:
        with open (filename, 'r') as file:  #open the file
            for line in file:
                u, p, lt, w, c, i, p1, p2, pt, hq, tc, cp, im, f, wh = line.strip().split(',')  #Read a line and split the values
                database[u] = [p, lt, w, c, i, p1, p2, pt, hq, tc, cp, im, f, wh]               #save the values in the dictionary
           
    except FileNotFoundError:
        pass

    print('database loaded.')
    return database

#Add a new user to database dictionary
def add_new_user(database, username, password):
    #'USERNAME': ['PASSWORD', LOGOUT_DATATIME, WOOD, CLAY, IRON, PROGRESS, PROGRESS2, PROGRESS_TIME, HEADQUARTES, TIMBERCAMP, CLAYPIT, IRONMINE, FARM, WAREHOUSE]
    database[username] = [password, datetime.now(), 500, 500, 500, -1, -1, 0, v.village[0].min_lv, v.village[1].min_lv, v.village[2].min_lv, v.village[3].min_lv, v.village[4].min_lv, v.village[5].min_lv]
    save_database(database)

#Load the user data from the dictionary database
def load_user_data(database, username):
    logout_time = datetime.strptime((database[username][1]), "%Y-%m-%d %H:%M:%S.%f")       #LOGOUT TIME    
    w = float(database[username][2])            #WOOD
    c = float(database[username][3])            #CLAY
    i = float(database[username][4])            #IRON
    p1 = database[username][5]                  #PROGRESS1
    p2 = database[username][6]                  #PROGRESS2
    pt = database[username][7]                  #PROGRESS TIME
    hq = database[username][8]                  #HEADQUARTES
    tc = database[username][9]                  #TIMBER CAMP
    cp = database[username][10]                  #CLAY PIT
    im = database[username][11]                 #ITON MINE
    f = database[username][12]                  #FARM
    wh = database[username][13]                 #WAREHOUSE 
    data = (logout_time, (w, c, i, p1, p2, pt, hq, tc, cp, im, f, wh))     #pack the data in a tuple
    return data

#save the data in the dictionary database
def update_user_data(database, username, current_time, data):
    w, c, i, p1, p2, pt, hq, tc, cp, im, f, wh = data       #unpack the data
    database[username][1] = current_time
    database[username][2] = w
    database[username][3] = c
    database[username][4] = i
    database[username][5] = p1
    database[username][6] = p2
    database[username][7] = pt
    database[username][8] = hq
    database[username][9] = tc
    database[username][10] = cp
    database[username][11] = im
    database[username][12] = f
    database[username][13] = wh


#Autosave timer
#def autosave(_time):
#    if datetime.now() > _time + start_autosave:
#        start_autosave = datetime.now()
#        return True
#save_database(user_database)
'---------------------------------------------------CLIENT--------------------------------------------------------'



#Client Thread
def client_conn(conn, addr):
    try:
        print('Connected to: ', addr)
        user_database = load_database()     #Load the database from the file
        print(user_database)
        
        send(conn, 'choise')                #send a msg to connected client
        while True:
            choice = read(conn)             #read the msg from the connectd client

            if not choice:                  #if is and empty str 
                break                       #close the thread
            
            #enter the login menu
            if choice == 'login':
                send(conn, 'username')      #ask for username and password
                username = read(conn)

                send(conn, 'password')
                password = read(conn)

                #if the username exists and the password match
                if username in user_database and user_database[username][0] == password:
                    send(conn, 'connected')

                    #logout_time, data = load_user_data(user_database, username)
                    #offline_time = datetime.now() - logout_time
                    #offline_seconds = offline_time.total_seconds()
                    #print(f'OFLINE: {offline_time}')
                    #print(f'OFLINE_S: {offline_seconds}')

                    g = Game(load_user_data(user_database, username))                                   #load the data from the user in dictionary database in the game
                    logged = True
                    state = 0
                    while logged:                                                                       #while client logged in the game
                        current_time = datetime.now()
                        upgrade_index = int(read(conn))                                                 #read Instructions from the client

                        if upgrade_index != -1:                                                         #check if is a valid instruction
                            if g.upgrade_avaliable(upgrade_index, g.village_level[upgrade_index]):      #if can upgrade
                                g.add_to_progress(upgrade_index)    


                        g.progress_countdown()                                                          #execute the progress

                        if g.delay(1):                                                                  #after a X time execute production
                            g.production()
                            state = 1 if state == 0 else 0                                              #update the game state

                        update_user_data(user_database, username, current_time, g.get_data())                         #update the dictionary database with values from game

                        if not send_data(conn, g.get_data(), state):                                    #if cannot send data to client
                            break                                                                       #close connection                                     #update and add the state to data
                                         
                        
                #if fail login
                else:
                    send(conn, 'invalid')
            #enter the register menu
            elif choice == 'register':
                send(conn, 'username')                                                                  #ask for username and password and confirm password
                username = read(conn)

                send(conn, 'password')
                password = read(conn)

                send(conn, 'password2')
                password2 = read(conn)

                if username in user_database:                                                           #if username already exists
                    send(conn, 'exists')
                elif password != password2:                                                             #if password dont match
                    send(conn, 'nomatch')
                else:                                                                                   #add the username and password to dictionary database
                    add_new_user(user_database, username, password)
                    send(conn, 'created')

    except socket.error as e:
        print(f"Error with client {addr}: {e}")
    finally:
        print('Disconnected from: ', addr)
        #logout_time = datetime.now()
        save_database(user_database)                                #save the database when client logout
        conn.close()    #close the connection withe the client

'-----------------------------------------------------------------------------------------------------------'
#start_autosave = datetime.now()

while True:                                
    conn, addr = server_socket.accept()     # Wait for a connection   

    # Create a new thread to handle the client
    conn_client = threading.Thread(target=client_conn, args=(conn, addr))
    conn_client.start() #start the thread

    #if autosave(5):                                                               #save the game after X time
    #    save_database(user_database)