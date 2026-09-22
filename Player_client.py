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
        print("Error: client has not been started.")
    else:
        clientSocket.close()
        print("Client has been closed.")

def getMessage():
    global clientSocket
    
    if clientSocket == None:
        print("Error: Client has not been started.")
        return False
    else:
        message = clientSocket.recv(1024)
        decodedMessage = message.decode()
        #print("Dealer says:", decodedMessage)
        return decodedMessage

def sendMessage(message):
    global clientSocket
    if clientSocket == None:
        print("Error: client socket has not been started or is not connected.")
    else: clientSocket.sendall(message.encode())


