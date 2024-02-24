import socket

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)     #connection type
        self.server = '127.0.0.1'                                           #server ip
        self.port = 5555                                                    #server port
        self.addr = (self.server, self.port)                                #address

    def connect(self):
        try:
            self.client.close()
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect(self.addr)
            print('Connected to: ', self.addr)
            return True
        except socket.error as e:
            print(e)
            return False


    def send(self, send_data):
        try:
            # Send a message to the client
            self.client.send(send_data.encode())
       
        except socket.error as e:
            print(e)
            return 'error'

    def read(self):
        try:
            #Read msg from server
            return self.client.recv(1024).decode()
        
        except socket.error as e:
            print(e)
            return 'error'
        
        #Send data and read from client
    def send_read(self, send_data):
        try:
            # Send a message to the client
            self.client.send(send_data.encode())
            #Read msg from server
            return self.client.recv(1024).decode()
        except socket.error as e:
            print(e)
            return 'error' 

    def read_send_data(self, send_data):
        try:
            data_pack = self.read()
            data_unpack = data_pack.split(',')
            read_data = tuple(map(str, data_unpack))

            self.send(send_data)
            return read_data
        except socket.error as e:
            print(e)
            return 'error'
    
    def read_send_state_data(self, send_data):
        try:
            state = self.read()
            self.send('state')

            data_pack = self.read()
            data_unpack = data_pack.split(',')
            read_data = tuple(map(str, data_unpack))
            self.send(send_data)

            return state, read_data
        except socket.error as e:
            print(e)
            return 'error'
    

    #def read_data(self):
    #    try:
    #        # Receive the message from the client
    #        data_pack = self.client.recv(1024).decode()
    #        #unpack the data
    #        data_unpack = data_pack.split(',')
    #        data_state = tuple(map(str, data_unpack)) 
    #        self.send('read') 
    #        data, state = get_state(data_state)
    #        return data, state
    #          
    #    except socket.error as e:
    #        print(e)
    #        return 'error'
        
#get and remove the last value from data
def get_state(data_state):
    state = int(data_state[0])     #get the value and convet to and integer
    data = data_state[1:]          #remove the value
    return data, state