'''
FTPClient.py will act as the clint connecting to the FTPServer.py. The Client will send a file that the server must copy, the name is then attaned from either one.
'''

import socket, sys, re
sys.path.append("../lib")# This for params.
import params
from Socket import * # This will hold our File transfer protocol.

switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-d', '--debug'), "debug", False), # Boolean (set if present) # No functionality has been given to switchesVarDefaults besides server.
    (('-?', '--usage'), "usage", False), # Boolean (set if present)
    )
progname = 'Client'
paramMap = params.parseParams(switchesVarDefaults)

server, usage, debug  = paramMap["server"], paramMap["usage"], paramMap["debug"]

if usage:
    params.usage()

try:
    serverHost, serverPort = re.split(':', server) # This will attain ip and port
    serverPort = int(serverPort) # This is the type cast
except: # This is the error case of the server
    pass
    myPrint('Cannot parse server:port from %s' %server)

addrFamily = socket.AF_INET # This is the IPV4
socktype = socket.SOCK_STREAM # This is TCP Connection
addrPort = (serverHost, serverPort) # This is tuple of server

s = socket.socket(addrFamily, socktype) # Create the socket

if s is None: # In case socket could not be made
    myPrint('Could not open socket')
    sys.exit(1)

try: # This will establish connection
    s.connect(addrPort)
    rcMsg = ftp_recv(s) # This is receive welcome message
    if 'hello' in rcMsg.lower(): # This is a hello message
        myPrint(rsMsg)

    fCopy = readLine() # This is file to copy
    fNewName = readLine() # This is new name for the file
    myPrint('Sending file Contents')

    ftp_send(s, fNewName, fCopy) # This will pass the socket, file to copy, and new name for file to be copied

except:
        myPrint('Could not connect to the server')
        sys.exit(1)
