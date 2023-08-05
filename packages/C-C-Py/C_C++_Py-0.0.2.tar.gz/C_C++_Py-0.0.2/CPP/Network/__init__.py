import socket
import pickle

class Network:
    def __init__(self,serverIP,port,id=None):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = serverIP#"192.168.1.77"
        self.port = port
        self.id = id
        self.index = []
        self.addr = (self.server, self.port)
        self.pos = self.connect()
        
        

    def getPos(self):
        return self.pos

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            pass

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)
    
    def sendObj(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048))
##                self.index.append(pickle.loads(self.client.recv(2048)))
##                print(self.index)
##                print(len(self.index + 'length'))

        except socket.error as e:
            print(e)
    
            
