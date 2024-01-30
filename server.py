#v.1.5.3
import socket
import threading
from game import Game
import village as v
'---------------------------------------------------CONNECTION--------------------------------------------------------'

#Create a server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Bind the socket to a specific IP and Port
server_ip = '127.0.0.1'
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
user_database = {
    #'USERNAME': ['PASSWORD', WOOD, CLAY, IRON, PROGRESS, PROGRESS2, PROGRESS_TIME, HEADQUARTES, TIMBERCAMP, CLAYPIT, IRONMINE, FARM, WAREHOUSE]
    'user': ['12345', 0, 0, 0, -1, -1, 0, 1, 1, 1, 1, 1, 1]
}

#Save the database in a file
def save_database(database, filename='user_database.txt'):
    try:
        with open(filename, 'w') as file:   #Open the file
            for u, data in database.items():
                p, w, c, i, p1, p2, pt, hq, tc, cp, im, f, wh = data
                file.write(f'{u},{p},{w},{c},{i},{p1},{p2},{pt},{hq},{tc},{cp},{im},{f},{wh}\n')    #write the values
                
    except FileNotFoundError:
        pass
    print('database saved.')

#Load the database from a file
def load_database(filename='user_database.txt'):
    database = {}   #Create an empty dictionary
    try:
        with open (filename, 'r') as file:  #open the file
            for line in file:
                u, p, w, c, i, p1, p2, pt, hq, tc, cp, im, f, wh = line.strip().split(',')  #Read a line and split the values
                database[u] = [p, w, c, i, p1, p2, pt, hq, tc, cp, im, f, wh]               #save the values in the dictionary
           
    except FileNotFoundError:
        pass

    print('database loaded.')
    return database

#Add a new user to database dictionary
def add_new_user(database, username, password):
    database[username] = [password, 500, 500, 500, -1, -1, 0, v.village[0].min_lv, v.village[1].min_lv, v.village[2].min_lv, v.village[3].min_lv, v.village[4].min_lv, v.village[5].min_lv]
    save_database(database)

#Load the user data from the dictionary database
def load_user_data(database, username):
    w = float(database[username][1])        #WOOD
    c = float(database[username][2])        #CLAY
    i = float(database[username][3])        #IRON
    p1 = database[username][4]              #PROGRESS1
    p2 = database[username][5]              #PROGRESS2
    pt = database[username][6]              #PROGRESS TIME
    hq = database[username][7]              #HEADQUARTES
    tc = database[username][8]              #TIMBER CAMP
    cp = database[username][9]              #CLAY PIT
    im = database[username][10]             #ITON MINE
    f = database[username][11]              #FARM
    wh = database[username][12]             #WAREHOUSE 
    data = (w, c, i, p1, p2, pt, hq, tc, cp, im, f, wh)     #pack the data in a tuple
    return data

#save the data in the dictionary database
def update_user_data(database, username, data):
    w, c, i, p1, p2, pt, hq, tc, cp, im, f, wh = data       #unpack the data
    database[username][1] = w
    database[username][2] = c
    database[username][3] = i
    database[username][4] = p1
    database[username][5] = p2
    database[username][6] = pt
    database[username][7] = hq
    database[username][8] = tc
    database[username][9] = cp
    database[username][10] = im
    database[username][11] = f
    database[username][12] = wh
    
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
                    g = Game(load_user_data(user_database, username))                                   #load the data from the user in dictionary database in the game
                    logged = True
                    state = 0
                    while logged:                                                                       #while client logged in the game
                        upgrade_index = int(read(conn))                                                 #read Instructions from the client

                        if upgrade_index != -1:                                                         #check if is a valid instruction
                            if g.upgrade_avaliable(upgrade_index, g.village_level[upgrade_index]):      #if can upgrade
                                g.add_to_progress(upgrade_index)                                        #add to progress
                        
                        g.progress_countdown()                                                          #execute the progress

                        if g.delay(1):                                                                  #after a X time execute production
                            g.production()
                            state = 1 if state == 0 else 0                                              #update the game state

                        #data = g.get_data()
                        update_user_data(user_database, username, g.get_data())                         #update the dictionary database with values from game

                        if not send_data(conn, g.get_data(), state):                                    #if cannot send data to client
                            break                                                                       #close connection                                     #update and add the state to data
                            
                        

                        if g.autosave(5):                                                               #save the game after X time
                            pass
                            #save_database(user_database)
                        
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
        conn.close()    #close the connection withe the client

'-----------------------------------------------------------------------------------------------------------'

while True:                                
    conn, addr = server_socket.accept()     # Wait for a connection   

    # Create a new thread to handle the client
    conn_client = threading.Thread(target=client_conn, args=(conn, addr))
    conn_client.start() #start the thread
    