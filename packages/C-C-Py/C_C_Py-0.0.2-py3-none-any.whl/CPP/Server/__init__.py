import socket 
from _thread import *
import sys
import pickle
class Server(object):
    def __init__(self,ServerIP,Port,MaxConnections,recieveBits=2048,type=None,id=1):
        self.type = type
        self.id = id
        self.recieveBits = recieveBits
        self.MaxConnections = MaxConnections
        
        self.server = ServerIP #"192.168.1.77"
        self.Port = Port #5555
        self.List = []

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        print("Server Created")


    def Run(self):
        try:
            self.s.bind((self.server, self.Port))
        except socket.error as e:
            str(e)

        self.s.listen(self.MaxConnections)
        print("Waiting for a connection, Server Started")


        while True:
            conn, addr = self.s.accept()
            print("Connected to:", addr)

            start_new_thread(self.threaded_client, (conn,))
    def read_pos(str):
        str = str.split(",")
        return int(str[0]), int(str[1])


    def make_pos(tup):
        return str(tup[0]) + "," + str(tup[1])
    def make_obj(obj):
        pickle.dump(obj)
    def read_obj(obj):
        pickle.load(obj)



    def threaded_client(self,conn):
        if self.type == None:
            conn.send(str.encode("Connected"))
            reply = ""
            while True:
                try:
                    data = conn.recv(2048)
                    reply = data.decode("utf-8")

                    if not data:
                        print("Disconnected")
                        break
                    else:
                        print("Received: ", reply)
                        print("Sending : ", reply)

                    conn.sendall(str.encode(reply))
                except:
                    break
        if self.type == 1:
            conn.send(str.encode("Connected"))
            reply = ""
            while True:
                try:
                    data = conn.recv(2048)
                    reply = data.decode("utf-8")

                    if not data:
                        print("Disconnected")
                        break
                    else:
                        print("Received: ", reply)
                        print("Sending : ", reply)

                    conn.sendall(str.encode(self.make_pos(reply)))
                except:
                    break
        if self.type == 2:
            conn.send(str.encode("Connected"))
            reply = ""
            while True:
                try:
                    data = pickle.load(conn.recv(2048))
                    reply = data.decode("utf-8")

                    if not data:
                        print("Disconnected")
                        break
                    else:
                        print("Received: ", reply)
                        print("Sending : ", reply)

                    conn.sendall(str.encode(self.make_obj(reply)))
                except:
                    break
        if self.type == 3:
            pass
        

        print("Lost connection")
        conn.close()
    def Config(self,ServerIP,Port,MaxConnections,recieveBits=2048):
        self.ServerIP = ServerIP
        self.Port = Port
        self.MaxConnections = MaxConnections
        self.recieveBits = recieveBits
        print('Server information was changed changes')
        print('==========================================')
        print('IP:' + self.ServerIP)
        print('PORT:' + str(self.Port))
        print('MaxConnections:' + str(self.MaxConnections))
        print('Bits that can be Received:' + str(self.recieveBits))
        print('==========================================')
    
    def End(self):
        pass
    
        
    







