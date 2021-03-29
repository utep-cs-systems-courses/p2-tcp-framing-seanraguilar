import socket
from threading import Thread
from socketserver import ThreadingMixIn

ip = "127.0.0.1" # This is the ip address that we will use for the socket (binding)
port = 50001 # This is the port number that we will use for the socket (binding)
BUFFER_SIZE = 1024 # This is the size of bytes that we are going to be able to use

class ClientThread(Thread):

    def __init__(self,ip,port,sock):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.sock = sock
        print("New thread started for "+ ip +":" + str(port))

    def run(self):
        filename='mytext.txt'
        f = open(filename,'rb')
        while True:
            l = f.read(BUFFER_SIZE)
            while (l):
                self.sock.send(l)
                l = f.read(BUFFER_SIZE)
            if not l:
                f.close()
                self.sock.close()
                break

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #know this one
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #SOL_SOCKET is the level SO_REUSEADDR allows socket to forcibly bind to port in use by another socket with boolean value of true (1)
s.bind((ip, port)) #binding takes the params ip and port and adds info to socket
threads = [] # I know I need to implement mutex for each thread / the list of threads

while True:
    s.listen(2)
    print("Waiting for incoming connections...")
    connection, (ip,port) = s.accept() # This connects the clients using the ip and ports 
    print ('Got connection from ', (ip, port))
    newthread = ClientThread(ip, port, connection) # This creates a new thread for each client connection 
    newthread.start()
    threads.append(newthread) # This adds a thread to the list
    

for t in threads:
    t.join() # This will be the one that will seperate the threads in the list
connection.shutdown(socket.SHUT_WR)
connection.close() 
