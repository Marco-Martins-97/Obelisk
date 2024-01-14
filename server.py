#v.1.0
import socket
import threading

#Create a server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Dind the socket to a specific IP and Port
server_ip = '127.0.0.1'
server_port = 5555
server_socket.bind((server_ip, server_port))

#Listen for incoming connections
server_socket.listen(5)
print(f"Server listening on {server_ip}:{server_port}")


def send(conn, msg):

    # Send a message to the client
    conn.send(msg.encode())
    
def read(conn):
    # Receive the message from the client
    return conn.recv(1024).decode()

def client_conn(conn, addr):
    print('Connected from: ', addr)

    msg = 'Connected'
    send(conn, msg)
    conn.close()


while True:                                
    conn, addr = server_socket.accept()     # Wait for a connection   

    # Create a new thread to handle the client
    conn_client = threading.Thread(target=client_conn, args=(conn, addr))
    conn_client.start()
    