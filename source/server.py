import socket, sys, re # Import socket module

ip = "127.0.0.1" # This is the ip address that we will use for the socket (binding)
port = 50001 # This is the port number that we will use for the socket (binding)
BUFFER_SIZE = 1024 # This is the size of bytes that we are going to be able to use

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a socket object
s.bind((ip, port)) # Bind to the socket that we created that will store the ip and port
s.listen(5) # This is where the server will be waiting for client to connect to the socket

print('Server Listening For Connection...')

while True:
    connection, address = s.accept() # This is where we establish that there was a connection with client
    print('Got Connection From: ', address) 
    data = connection.recv(BUFFER_SIZE).decode('utf-8') # This is where we are going recieve our data and decode it into bytes
    print('Data in file: ', (data))  
    #print('Server received: ', repr(data)) # repr returns a string that contains a printable representation of the object

with open('recieveFile', 'wb') as f:
    print('File Opened')
    f.close()

connection.shutdown(socket.SHUT_WR)
connection.close()
s.close()
print('Connection Is Closed!') 
