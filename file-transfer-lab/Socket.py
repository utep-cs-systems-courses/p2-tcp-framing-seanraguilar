'''
FTPSock.py is going to represent our own custom transfer protocol. Its main use is for file transfer from the Client to Server. It should be taking in user input which is a file name, transfer its data
and then the Server will create the file and copy the data into it. Here we will simply define the send and recv of our protocol.
'''

import re, os, sys
import socket

def readLine(): # This reads line \ functions like input
    return os.read(0,1024).decode()

def myPrint(string): # Takes the string and prints onto string
    os.write(1, (string + '\n').encode())

def myOpen(fileName): #open our files to be able to read them
    try:
        fd_in = os.open(fileName, os.O_RDWR) #open and read the file
        rBuf = os.read(fd_in,1024)
        os.close(fd_in)
        return rBuf #buffer of what has been read
    except FileNotFoundError:
        myPrint('File was not found')
        sys.exit(1)

def myWrite(fileName, wBuf): #custom write to file method
    fd_out = os.open(fileName, os.O_WRONLY | os.O_CREAT) #output file descriptor | open if existing / create if not
    os.write(fd_out, wBuf.encode()) #writing to the file
    os.close(fd_out)

def ftp_send(sock, outFile, inFile): #socket gives us all the necessary information
    fCont = myOpen(inFile)
    sock.send((outFile + '\n').encode()) #first send the file name you would like
    while '\n' in fCont: #iterate thourgh every line
        msg = fCont[:fCont.index('\n')]
        fCont = fCont[fCont.index('\n')]
        sock.send((msg + '\n').encode()) #send an endline terminator
    sock.send('.') #terminator

def ftp_recv(sock):
    fCont = '' #buffer for receiver
    while '.' not in fCont:
        fCont = fCont + sock.recv(1024) #attain entire message
    return fCont.decode()

def ftp_handleIn(fCont): #handle the content, identify what it is
    if 'Hello' in fCont: #initial connection greeting
        myPrint(fCont)
    else: #filename with contents
        fileName = fCont.split('\n')[0] #file we want to write
        #pass the fileName | split string to get contents by taking last letter of fileName +2 to account for new line char
        myWrite(fileName, fCont[fCont.index(fileName[-1])+2:])
