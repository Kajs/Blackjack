import socket
import time

clientSocket = None
myPlayerName = None
dealerHand = []
myHand = []

def startClient(host, port):
    global clientSocket
    
    print("Starting client.")
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((host, port))
    print("Client ready.")

def closeClient():
    global clientSocket

    if clientSocket == None:
        print("Error in closeClient: client has not been started.")
    else:
        clientSocket.close()
        print("Client has been closed.")

#wait for a server text command and return it
def getMessage():
    global clientSocket
    
    if clientSocket == None:
        print("Error in getMessage: client has not been started.")
        return False
    else:
        message = clientSocket.recv(1024)
        decodedMessage = message.decode()
        #print("Dealer says:", decodedMessage)
        return decodedMessage

#Send a response to the server
def sendMessage(message):
    global clientSocket
    if clientSocket == None:
        print("Error in sendMessage: client socket has not been started or is not connected.")
    else: clientSocket.sendall(message.encode())


