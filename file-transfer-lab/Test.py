import os

def readLine():
    return os.read(0,1024).decode()

def myPrint(string):
    os.write(1, (string + '\n').encode())

def myOpen(fileName):
    fd_in = os.open(fileName, os.O_RDWR | os.O_CREAT) # Opens and reads the file
    #os.set_inheritable(0, True) # This changes the file descriptor input
    myPrint((os.read(fd_in,1024)).decode())
    os.close(fd_in)

def myWrite(fileName, wBuf):
    fd_out = os.open(fileName, os.O_WRONLY | os.O_CREAT)
    os.write(fd_out, wBuf.encode())
    os.close(fd_out)

t = readLine()
myOpen(t[:t.index('\n')]) 
