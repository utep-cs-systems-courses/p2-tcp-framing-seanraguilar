import socket, sys, re # Import socket module

ip = "127.0.0.1" # This is the ip address that we will use for the socket (binding)
port = 50001 # This is the port number that we will use for the socket (binding)
BUFFER_SIZE = 1024 # This is the size of bytes that we are going to be able to use

# I have to create a header here ()
# He likes a byte array
# Byte array (out of bound framming) header:contents


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

'''
#Framing here:
    try:

        # Receive our "header" containing message length, it's size is defined and constant
        message_header = client_socket.recv(HEADER_LENGTH)

        # If we received no data, client gracefully closed a connection, for example using socket.close() or socket.shutdown(socket.SHUT_RDWR)
        if not len(message_header):
            return False

        # Convert header to int value
        message_length = int(message_header.decode('utf-8').strip())

        # Return an object of message header and message data
        return {'header': message_header, 'data': client_socket.recv(message_length)}

    except:

        # If we are here, client closed connection violently, for example by pressing ctrl+c on his script
        # or just lost his connection
        # socket.close() also invokes socket.shutdown(socket.SHUT_RDWR) what sends information about closing the socket (shutdown read/write)
        # and that's also a cause when we receive an empty message
        return False '''
