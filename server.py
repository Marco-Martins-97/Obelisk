#v.1.2
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
    'user2': '123',
}
'---------------------------------------------------CLIENT--------------------------------------------------------'

def client_conn(conn, addr):
    print('Connected to: ', addr)
    login = True
    while login:
        send(conn, 'username')
        username = read(conn)

        send(conn, 'password')
        password = read(conn)

        if username in user_database and user_database[username] == password:
            send(conn, 'connected')
            login = False
        else:
            send(conn, 'invalid')
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
    