#v.1.5.1
import socket
import threading
from game import Game
import village as v
'---------------------------------------------------CONNECTION--------------------------------------------------------'

#Create a server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Dind the socket to a specific IP and Port
server_ip = '127.0.0.1'
server_port = 5555
server_socket.bind((server_ip, server_port))

#Listen for incoming connections
server_socket.listen(5)
print(f"Server listening on {server_ip}:{server_port}")

'---------------------------------------------------DATA--------------------------------------------------------'

def send(conn, data):
    try:
        # Send a message to the client
        conn.send(data.encode())
    except socket.error as e:
            print(e)  

def read(conn):
    try:
        # Receive the message from the client
        return conn.recv(1024).decode()
    except socket.error as e:
            print(e)

def send_data(conn, data):
    try:
        #pack the data
        data_pack = ','.join(map(str, data))
        # Send a message to the client
        conn.send(data_pack.encode())
        return read(conn)
    except socket.error as e:
            print(e)

# def read_data(conn):
#     try:
#         # Receive the message from the client
#         data_pack = conn.recv(1024).decode()
#         #unpack the data
#         data_unpack = data_pack.split(',')
#         data = tuple(map(int, data_unpack))
        
#         return data
#     except socket.error as e:
#         print(e)
'---------------------------------------------------DATABASE--------------------------------------------------------'

user_database = {
    #'USERNAME': ['PASSWORD', WOOD, CLAY, IRON, PROGRESS, PROGRESS2, PROGRESS_TIME, HEADQUARTES, TIMBERCAMP, CLAYPIT, IRONMINE, FARM, WAREHOUSE]
    'user': ['12345', 0, 0, 0, -1, -1, 0, 1, 1, 1, 1, 1, 1]
}


def save_database(database, filename='user_database.txt'):
    try:
        with open(filename, 'w') as file:
            for u, data in database.items():
                p, w, c, i, p1, p2, pt, hq, tc, cp, im, f, wh = data
                file.write(f'{u},{p},{w},{c},{i},{p1},{p2},{pt},{hq},{tc},{cp},{im},{f},{wh}\n')
                
    except FileNotFoundError:
        pass
    print('database saved.')

def load_database(filename='user_database.txt'):
    database = {}
    try:
        with open (filename, 'r') as file:
            for line in file:
                u, p, w, c, i, p1, p2, pt, hq, tc, cp, im, f, wh = line.strip().split(',')
                database[u] = [p, w, c, i, p1, p2, pt, hq, tc, cp, im, f, wh]
           
    except FileNotFoundError:
        pass

    print('database loaded.')
    return database

def add_new_user(database, username, password):
    database[username] = [password, 500, 500, 500, -1, -1, 0, v.village[0].min_lv, v.village[1].min_lv, v.village[2].min_lv, v.village[3].min_lv, v.village[4].min_lv, v.village[5].min_lv]
    save_database(database)

def load_user_data(database, username):
    w = float(database[username][1])
    c = float(database[username][2])
    i = float(database[username][3])
    p1 = database[username][4]
    p2 = database[username][5]
    pt = database[username][6]
    hq = database[username][7]
    tc = database[username][8]
    cp = database[username][9]
    im = database[username][10]
    f = database[username][11]
    wh = database[username][12]
    data = (w, c, i, p1, p2, pt, hq, tc, cp, im, f, wh)
    return data

def update_user_data(database, username, data):
    w, c, i, p1, p2, pt, hq, tc, cp, im, f, wh = data
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




def client_conn(conn, addr):
    try:
        print('Connected to: ', addr)
        user_database = load_database()
        print(user_database)
        
        send(conn, 'choise')
        while True:
            choice = read(conn)

            if not choice:
                break

            if choice == 'login':
                send(conn, 'username')
                username = read(conn)

                send(conn, 'password')
                password = read(conn)

                if username in user_database and user_database[username][0] == password:
                    send(conn, 'connected')
                    g = Game(load_user_data(user_database, username))
                    logged = True
                    while logged:
                        upgrade_index = int(read(conn))

                        if upgrade_index != -1:
                            if g.upgrade_avaliable(upgrade_index, g.village_level[upgrade_index]):      #the client do te same thing
                                g.add_to_progress(upgrade_index)
                        
                        g.progress_countdown()

                        if g.delay(1):
                            g.production()

                        update_user_data(user_database, username, g.get_data())


                        if not send_data(conn, g.get_data()):
                            break

                        if g.autosave(5):
                            save_database(user_database)
                else:
                    send(conn, 'invalid')
                    print(user_database)
                    print(username, password)

            elif choice == 'register':
                send(conn, 'username')
                username = read(conn)

                send(conn, 'password')
                password = read(conn)

                send(conn, 'password2')
                password2 = read(conn)

                if username in user_database:
                    send(conn, 'exists')
                elif password != password2:
                    send(conn, 'nomatch')
                else:
                    add_new_user(user_database, username, password)
                    send(conn, 'created')

                    print(username, password)
                    print(user_database)
    except socket.error as e:
        print(f"Error with client {addr}: {e}")
    finally:
        print('Disconnected from: ', addr)
        conn.close()





'-----------------------------------------------------------------------------------------------------------'

while True:                                
    conn, addr = server_socket.accept()     # Wait for a connection   

    # Create a new thread to handle the client
    conn_client = threading.Thread(target=client_conn, args=(conn, addr))
    conn_client.start()
    