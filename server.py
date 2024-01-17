#v.1.4
import socket
import threading
from game import Game
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

def send(conn, msg):

    # Send a message to the client
    conn.send(msg.encode())
    
def read(conn):
    # Receive the message from the client
    return conn.recv(1024).decode()
'---------------------------------------------------DATABASE--------------------------------------------------------'

user_database = {
    'user': ['12345', 0, 0, 0]
}


def save_database(database, filename='user_database.txt'):
    with open(filename, 'w') as file:
        for u, data in database.items():
            p, w, c, i = data
            file.write(f'{u},{p},{w},{c},{i}\n')
            
    print('database saved.')

def load_database(filename='user_database.txt'):
    database = {}
    try:
        with open (filename, 'r') as file:
            for line in file:
                u, p, w, c, i = line.strip().split(',')
                database[u] = [p, w, c, i]
           
    except FileNotFoundError:
        pass

    print('database loaded.')
    return database

def add_new_user(database, username, password):
    database[username] = [password, 0, 0, 0]
    save_database(database)

def load_user_data(database, username):
    w = database[username][1]
    c = database[username][2]
    i = database[username][3]
    return w, c, i

def update_user_data(database, username, w, c, i):
    database[username][1] = w
    database[username][2] = c
    database[username][3] = i
    save_database(database)
    
#save_database(user_database)
'---------------------------------------------------CLIENT--------------------------------------------------------'




def client_conn(conn, addr):
    print('Connected to: ', addr)
    user_database = load_database()
    print(user_database)
    
    send(conn, 'choise')
    while True:
        choice = read(conn)
        if choice == 'login':
            send(conn, 'username')
            username = read(conn)

            send(conn, 'password')
            password = read(conn)

            if username in user_database and user_database[username][0] == password:
                send(conn, 'connected')
                w, c, i = load_user_data(user_database, username)
                print(w,c,i)
                g = Game(w,c,i)
                logged = True
                while logged:
                    if g.delay(1):
                        g.production()
                    if g.autosave(5):
                        w, c, i = g.save_data()
                        update_user_data(user_database, username, w, c, i)
                break
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

        
    conn.close()
    print('Disconnected from: ', addr)





'-----------------------------------------------------------------------------------------------------------'

while True:                                
    conn, addr = server_socket.accept()     # Wait for a connection   

    # Create a new thread to handle the client
    conn_client = threading.Thread(target=client_conn, args=(conn, addr))
    conn_client.start()
    