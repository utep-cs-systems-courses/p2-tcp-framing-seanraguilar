import socket, sys, re, os

ip = "127.0.0.1" # This is the ip address that we will use for the socket (binding)
port = 50001 # This is the port number that we will use for the socket (binding)
BUFFER_SIZE = 1024 # This is the size of bytes that we are going to be able to use

# I have to create a header here ()
#HEADER_SIZE = len(message) 
#message_header = f"{len(message)}".encode('utf-8')
#client_socket.send(message_header + ':'.encode() + message)

'''
Framming:
# Encode message to bytes, prepare header and convert to bytes, like for username above, then send
message = message.encode('utf-8')
message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(message_header + message)
'''


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creating a socket for the client to connect
s.connect((ip, port)) # Connecting the ip and port to the socket
fileName = input()

fileName = 'test.txt' # The file that we will be opening that will be sent to the server through the socket
f = open(fileName, 'rb')
l = f.read(BUFFER_SIZE)

while (l):
    s.send(l) # Sending the message to the server!
    print('Sent: ', repr(l)) # repr returns a string of the data / object
    l = f.read(BUFFER_SIZE)
    f.close()
    break
f.close()

print('Successfully sent the file!')
s.shutdown(socket.SHUT_WR)

s.close()
print('Connection closed!') 
