import socket

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)     #tipo de conecçao
        self.server = '127.0.0.1'                                           #server ip
        self.port = 5555                                                    #server port
        self.addr = (self.server, self.port)                                #endereço
        #self.u = self.connect()                                             #conecta ao user

    def connect(self):
        try:
            self.client.connect(self.addr)

        except socket.error as e:
            print(e)
        
    def send(self, msg):
        try:
            # Send a message to the client
            self.client.sendall(msg.encode())
       
        except socket.error as e:
            print(e)

    def read(self):
        try:
            return self.client.recv(1024).decode()
        
        except socket.error as e:
            print(e)