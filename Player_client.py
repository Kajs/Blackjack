import socket
import time

clientSocket = None
myPlayerName = None
dealerHand = []
myHand = []

def setMyPlayerName(playerName):
    global myPlayerName
    
    if myPlayerName == None:
        myPlayerName = playerName
        print("I am " + myPlayerName)
    else: print("ERROR: my player name has already been set.")

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
        print("Dealer says:", decodedMessage)
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
    global myPlayerName
    
    if ':' in message:
        messageParts = message.split(":", 1)

        messageType = messageParts[0].strip()
        messageValue = messageParts[1].strip()

        #print("Message type:", messageType, "MessageValue", messageValue)

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
        if messageType == "YOURNAMEIS":
            setMyPlayerName(messageValue)
        if messageType == "UPDATE":
            hands = messageValue.split(";")
            for i in range(len(hands) - 1): #skipping the last terminating ';'
                handString = hands[i]
                handParts = handString.split(':', 1)
                handType = handParts[0].strip()
                cards = handParts[1].strip()

                if handType == "DEALER":
                    print("Dealer hand: " + cards)
                elif handType == myPlayerName:
                    print("My hand: " + cards)
                else: print("ERROR parsing hand")
                #print("Update request:",i,hands[i])
    else: print("Error: invalid format in message:", message)
    return True
