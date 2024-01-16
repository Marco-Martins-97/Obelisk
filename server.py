#v.1.3.1
import socket
import threading
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
    'user': '12345',
}
#save_database(user_database)

def save_database(database, filename='user_database.txt'):
    with open(filename, 'w') as file:
        for u, p in database.items():
            file.write(f'{u},{p}\n')
            
    print('database saved.')

def load_database(filename='user_database.txt'):
    database = {}
    try:
        with open (filename, 'r') as file:
            for line in file:
                u, p = line.strip().split(',')
                database[u] = p
                
    except FileNotFoundError:
        pass

    print('database loaded.')
    return database
'---------------------------------------------------CLIENT--------------------------------------------------------'




def client_conn(conn, addr):
    print('Connected to: ', addr)
    user_database = load_database()
    
    send(conn, 'choise')
    while True:
        choice = read(conn)
        if choice == 'login':
            send(conn, 'username')
            username = read(conn)

            send(conn, 'password')
            password = read(conn)

            if username in user_database and user_database[username] == password:
                send(conn, 'connected')
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
                user_database[username] = password
                save_database(user_database)
                send(conn, 'created')

                print(user_database)
                print(username, password)

        
    conn.close()
    print('Disconnected from: ', addr)





'-----------------------------------------------------------------------------------------------------------'

while True:                                
    conn, addr = server_socket.accept()     # Wait for a connection   

    # Create a new thread to handle the client
    conn_client = threading.Thread(target=client_conn, args=(conn, addr))
    conn_client.start()
    