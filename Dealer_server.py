import socket

serverAddress = "127.0.0.1"
serverPort = 5000
serverSocket = None
clients = {}
validActions = ["ACTION: HIT", "ACTION: STAND", "ACTION: QUIT"]
playerNumber = 0

def getMessage(playerNumber):  #Wait for a response from a player client and return it
    global serverSocket
    global clients  

    if playerNumber in clients:
        connection, address = clients[playerNumber]
        message = connection.recv(1024)
        decodedMessage = message.decode()
        #print(playerNumberToName(playerNumber) + " says:", decodedMessage)
        return decodedMessage
    else: print("Error in getMessage: playerNumber does not exist in clients.")        

def sendMessage(playerNumber, message):  #Send a text command to a player client
    global clients

    if playerNumber in clients:
        connection, address = clients[playerNumber]
        connection.sendall(message.encode())
    else: print("Error in sendMessage: playerNumber does not exist in clients.") 

def playerNumberToName(playerNumber): return ("PLAYER" + str(playerNumber))

def sendPlayerNumber(playerNumber):  #Tell a player client what name and number it's been assigned on the server side
    global clients

    if playerNumber in clients:
        message = "YOURNUMBERIS: " + str(playerNumber) + '\n'
        sendMessage(playerNumber, message)
    else: print("Error in sendPlayerNumber: playerNumber does not exist in clients.") 

def startServer(host, port):
    global serverSocket
    print("Starting server.")
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind((host, port))
    serverSocket.listen(1)
    print("Server is now listening at " + host + ':' + str(port))

def closeServer():
    global serverSocket
    if serverSocket == None:
        print("Error in closeServer: server socket has not been started.")
    else:
        print("Closing server socket.")
        serverSocket.close()
        print("Server socket has been closed.")

def acceptConnection():  #Wait for a player to connect, assign the player a number and send it to the player client
    global clients
    global serverSocket
    global playerNumber

    if serverSocket == None:
        print("Error in acceptConnection: server socket has not been started")
    else:
        print("Waiting for player to connect...")
        connection, address = serverSocket.accept()
        playerNumber += 1
        print(playerNumberToName(playerNumber) + " connected:", address, '\n')
        clients[playerNumber] = (connection, address)
        sendPlayerNumber(playerNumber)
        return playerNumber
    return -1

def closeConnection(playerNumber):   #End the connection to a specific player
    global clients

    if playerNumber in clients:
        connection, address = clients[playerNumber]
        connection.close()
        del clients[playerNumber]
        print(playerNumberToName(playerNumber) + " has been disconnected.")
    else: print("Error in closeConnection: playerNumber does not exist in clients.")  

def requestAction(playerNumber):  #Send an a request for the player to take an action (such as hit or stand), to the players client
    global validActions
    sendMessage(playerNumber, "REQUEST: ACTION\n")
    action = getMessage(playerNumber)
    if action in validActions: return action
    else:
        print("ERROR in requestAction: invalid action:", action)
        return ("ERROR: Invalid action: " + str(action))

def requestClose(playerNumber): sendMessage(playerNumber, "REQUEST: CLOSE\n")   #Tell the player client to close it's connection and gui

def updatePlayerBoard(playerNumber, dealerHand, playerHand):   #Send the contents of the dealers hand and the players hand to the player client in text format 
    message = "UPDATE:"
    message += "DEALER:" + dealerHand + ';'
    message += playerNumberToName(playerNumber) + ':' + playerHand + '\n'
    sendMessage(playerNumber, message)
