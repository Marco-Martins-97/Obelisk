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
            return True

        except socket.error as e:
            print(e)
            return False
        
    def disconnect(self):
        try:
            self.client.close()

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

    def read_data(self):
        try:
            # Receive the message from the client
            data_pack = self.client.recv(1024).decode()
            #unpack the data
            data_unpack = data_pack.split(',')
            data = tuple(map(float, data_unpack)) 
            self.send('read') 
            return data
        
        
        except socket.error as e:
            print(e)
            return None

