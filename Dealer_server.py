import socket

serverAddress = "127.0.0.1"
serverPort = 5000
serverSocket = None
clients = {}
validActions = ["ACTION: HIT", "ACTION: STAND", "ACTION: QUIT"]
playerNumber = 0

#Wait for a response from a player client and return it
def getMessage(playerNumber):
    global serverSocket
    global clients  

    if playerNumber in clients:
        connection, address = clients[playerNumber]
        message = connection.recv(1024)
        decodedMessage = message.decode()
        #print(playerNumberToName(playerNumber) + " says:", decodedMessage)
        return decodedMessage
    else: print("Error in getMessage: playerNumber does not exist in clients.")        

#Send a text command to a player client
def sendMessage(playerNumber, message):
    global clients

    if playerNumber in clients:
        connection, address = clients[playerNumber]
        connection.sendall(message.encode())
    else: print("Error in sendMessage: playerNumber does not exist in clients.") 

#Get a string version of a playername from the players number
def playerNumberToName(playerNumber):
    playerName = "PLAYER" + str(playerNumber)
    return playerName

#Tell a player client what number it's been assigned on the server side
def sendPlayerName(playerNumber):
    global clients

    if playerNumber in clients:
        playerName = playerNumberToName(playerNumber)
        message = "YOURNAMEIS: " + playerName + '\n'
        sendMessage(playerNumber, message)
    else: print("Error in sendPlayerName: playerNumber does not exist in clients.") 

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

#Wait for a player to connect, assign the player a number and send it to the player client
def acceptConnection():
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
        sendPlayerName(playerNumber)
        return playerNumber
    return -1

#End the connection to a specific player
def closeConnection(playerNumber):
    global clients

    if playerNumber in clients:
        connection, address = clients[playerNumber]
        connection.close()
        del clients[playerNumber]
        print(playerNumberToName(playerNumber) + " has been disconnected.")
    else: print("Error in closeConnection: playerNumber does not exist in clients.")  

 
#Send an a request for the player to take an action (such as hit or stand), to the players client
def requestAction(playerNumber):
    global validActions
    sendMessage(playerNumber, "REQUEST: ACTION\n")
    action = getMessage(playerNumber)
    if action in validActions: return action
    else:
        print("ERROR in requestAction: invalid action:", action)
        return ("ERROR: Invalid action: " + str(action))

#Tell the player client to close it's connection and gui
def requestClose(playerNumber): sendMessage(playerNumber, "REQUEST: CLOSE\n")

#Send the contents of the dealers hand and the players hand to the player client in text format 
def updatePlayerBoard(playerNumber, dealerHand, playerHand):
    message = "UPDATE:"
    message += "DEALER:" + dealerHand + ';'
    message += playerNumberToName(playerNumber) + ':' + playerHand + '\n'
    sendMessage(playerNumber, message)
