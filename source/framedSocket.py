'''This is where the magic happens, framing the message to be able to send and recieve the message!'''
import re

def frameSend(sock, fileName, fileData):
    #frame ex:   filelength:test.txt:filedata
    msg = str(len(fileData)).encode() + b':' + fileName.encode() + b':' + fileData
    while len(msg):
        sentMsg = sock.send(msg) # This will continuously send file contents
        msg = msg[sentMsg:] # This will cut message length (framing)
    
rbuff = b""
def frameRecv(sock):
    global rbuff
    state = 1
    msgLength = -1
    while True:
        if state == 1:
            # Used regex to split string into three parts for our variables
            match = re.match(b'([^:]+):(.*):(.*)', rbuff, re.DOTALL | re.MULTILINE)
            if match:
                strLength, fileName, rbuff = match.groups() # Set variables from regex groups
                try:
                    msgLength = int(strLength)
                except:
                    if len(rbuff):
                        print("Message Incorrectly Formatted")
                        return None, None
                state = 2
                
        if state == 2: # This starts sending the file's contents and the file name
            if len(rbuff) >= msgLength: # Once we have all file content, then we send it
                fileData = rbuff[0:msgLength] # This is the start of framing
                rbuff = rbuff[msgLength:] # This is the end of framing the message
                return fileName, fileData
            
        recMessage = sock.recv(1024) # This receives data and puts it in buffer 
        rbuff += recMessage
        if len(recMessage) == 0:# If nothing is received and the buffer still has content, then quit
            if len(rbuff) != 0:
                print("Incomplete Message")
            return None, None
