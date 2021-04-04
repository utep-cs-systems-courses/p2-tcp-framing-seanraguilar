''''''
import socket, sys, re, time, os
sys.path.append("../lib") # For params
import params
from framedSocket import frameSend
switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-d', '--debug'), 'debug', False),
    (('-?', '--usage'), "usage", False), # Boolean (set if present)
    )


progname = "client"
paramMap = params.parseParams(switchesVarDefaults)

server, usage, debug  = paramMap["server"], paramMap["usage"], paramMap["debug"]

if usage:
    params.usage()

try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

s = None
port = (serverHost, serverPort) 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Establishing connection with the socket
s.connect(port) # Connecting to socket

if s is None:
    print('Could Not Open Socket')
    sys.exit(1)
    
FILE_PATH ="clientFiles/" # To get access of our client files

while True:
    print("Enter File Name: ")
    fileName = os.read(0, 1024).decode()
    filePath = (FILE_PATH + fileName).strip()
    if fileName != "exit":
        if os.path.isfile(filePath): # Checks the whole path if the file is a actually a file
            print("Sending File Contents")
            file = open(filePath, "rb") # This is reading in binary mode
            fileData = file.read()
            if len(fileData) < 1: # This can't handle empty files
                print("Empty File, Try Again")
                continue
            frameSend(s, fileName, fileData) # This will send the file and file contents
        else:
            print("File Does Not Exist Try Again")
            s.close() # This will close connection in order to open it up 
            sys.exit(1)
        if int(s.recv(1024).decode()) == 1: # This is if the file successfully transfered
            print("server received file")
            s.close()
            sys.exit(0)
        else: # This is if the file unsuccessfully transfered
            print("Server Failed in Receiving File")
            s.close()
            sys.exit(1)
    else:
        print("Exiting")
        s.close()
        sys.exit(0)
