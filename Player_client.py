import socket
import time

serverAddress = "127.0.0.1"
serverPort = 5000
clientSocket = None
clientActive = False

def startClient(host, port):
    global clientSocket
    global clientActive
    
    print("Starting client.")
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((host, port))
    clientActive = True
    print("Client ready.")

def closeClient():
    global clientSocket
    global clientActive

    if clientSocket == None:
        print("Error: client has not been started.")
    else:
        clientSocket.close()
        clientActive = False
        print("Client has been closed.")

def getMessage():
    global clientSocket
    
    if clientSocket == None:
        print("Error: Client has not been started.")
    else:
        message = clientSocket.recv(1024)
        decodedMessage = message.decode()
        print("Dealer says:", decodedMessage)
        parseMessage(decodedMessage)

def sendMessage(message):
    global clientSocket
    if clientSocket == None:
        print("Error: client socket has not been started or is not connected.")
    else: clientSocket.sendall(message.encode())

def getPlayerAction():
    response = ""
    while response != 's':
        response = input()
        if response == "h":
            print ("Sending HIT")
            return "HIT"
        if response == "s":
            print ("Sending STAY")
            return "STAY"
        else: print("ERROR: invalid input: " + response)

def parseMessage(message):
    if ':' in message:
        messageParts = message.split(":", 1)

        messageType = messageParts[0].strip()
        messageValue = messageParts[1].strip()

        print("Message type:", messageType, "MessageValue", messageValue)

        if messageType == "REQUEST":
            if messageValue == "ACTION":
                action = getPlayerAction()
                if action == "HIT": sendMessage("ACTION: HIT")
                elif action == "STAY": sendMessage("ACTION: STAY")
                else: print("ERROR: invalid action: " + action)
            if messageValue == "CLOSE": closeClient()
    else: print("Error: invalid format in message:", message)





startClient(serverAddress, serverPort)
while clientActive: getMessage()
#getMessage()
#sendMessage("Hello from Player 1.")
#closeClient()
