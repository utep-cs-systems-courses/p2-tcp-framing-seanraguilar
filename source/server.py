''''''
import socket, sys, re, os
sys.path.append("../lib")
import params
from threading import Thread
from socketserver import ThreadingMixIn
from framedSocket import frameRecv
switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-?', '--usage'), "usage", False),
    (('-d', '--debug'), "debug", False),
    )

progname = "server"
paramMap = params.parseParams(switchesVarDefaults)

listenPort = paramMap['listenPort']
listenAddr = '' # Symbolic name meaning all available interfaces

debug = paramMap['debug']

if paramMap['usage']:
    params.usage()

class ClientThread(Thread): # This is a class that will help creating threads of other clients
    def __init__(self,ip,port,sock):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.sock = sock
        print("New thread started for "+ip+":"+str(port))
        
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Establishing the socket which we indicated as "s"
bindAddress = ("127.0.0.1", listenPort) 
s.bind(bindAddress) # This is is where we bind the ip and the port
s.listen(10) # This will allow only one outstanding request and s is a factory for connected sockets
threads = [] # need to change to set() for mutex

os.chdir("./serverFiles") # This is where our transferred files will be located
while True:
    print("Waiting for connection...") 
    conn, (addr,port) = s.accept() # Accepting the connection and address of the socket
    if os.fork() == 0:
        print('Connected successful! Connected to ', (addr,port))
        newthread = ClientThread(addr,port,conn) # This creates a new thread for each client connection
        newthread.start()
        threads.append(newthread) # This adds to the threads to list that we created threads = []
        try:
            print("Waiting for client connection...") # Indication that we are waiting to receive file name and its contents
            fileName, fileData = frameRecv(conn) # This is where we start receiving file and its contents
            print("Successfully received data: ", fileName, " from client : ", (addr, port))
        except:
            print("Failed data transfer")
            conn.send(("0").encode()) # Indication that the data transfer failed to receive
            sys.exit(1)
            
        fileName = fileName.decode()
        try:
            transferFile = open(fileName, "wb") # This will write in binary mode ("wb")
            transferFile.write(fileData)
            transferFile.close()
        except:
            print("Failed to write to file")
            conn.send(("0").encode()) # Indication that it failed to write (using the number "0")
            sys.exit(1)
        for t in threads:
            t.join() # This will be the one that will seperate the threads in the list   
        conn.send(("1").encode()) # Indication that it successfully transfered the file (using "1")
        sys.exit(0)
