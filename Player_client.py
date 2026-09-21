import socket
import time

clientSocket = None

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
        return parseMessage(decodedMessage)

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
            print ("Sending STAND")
            return "STAND"
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
                elif action == "STAND": sendMessage("ACTION: STAND")
                else: print("ERROR: invalid action: " + action)
                return True
            if messageValue == "CLOSE":
                closeClient()
                return False
    else: print("Error: invalid format in message:", message)
    return True
