import socket

serverAddress = "127.0.0.1"
serverPort = 5000
serverSocket = None
clients = {}
validActions = ["ACTION: HIT", "ACTION: STAND", "ACTION: QUIT"]
playerNumber = 0

def getMessage(playerNumber):
    global serverSocket
    global clients  

    if playerNumber in clients:
        connection, address = clients[playerNumber]
        message = connection.recv(1024)
        decodedMessage = message.decode()
        #print(playerNumberToName(playerNumber) + " says:", decodedMessage)
        return decodedMessage
    else: print("Error: playerNumber does not exist in clients.")        

def sendMessage(playerNumber, message):
    global clients

    if playerNumber in clients:
        connection, address = clients[playerNumber]
        connection.sendall(message.encode())
    else: print("Error: playerNumber does not exist in clients.") 

def playerNumberToName(playerNumber):
    playerName = "PLAYER" + str(playerNumber)
    return playerName

def sendPlayerName(playerNumber):
    global clients

    if playerNumber in clients:
        playerName = playerNumberToName(playerNumber)
        message = "YOURNAMEIS: " + playerName + '\n'
        sendMessage(playerNumber, message)
    else: print("Error: playerNumber does not exist in clients.") 

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
        print("Error: Server socket has not been started.")
    else:
        print("Closing server socket.")
        serverSocket.close()
        print("Server socket has been closed.")

def acceptConnection():
    global clients
    global serverSocket
    global playerNumber

    if serverSocket == None:
        print("Error: Server socket has not been started")
    else:
        print("Waiting for player to connect...")
        connection, address = serverSocket.accept()
        playerNumber += 1
        print(playerNumberToName(playerNumber) + " connected:", address, '\n')
        clients[playerNumber] = (connection, address)
        sendPlayerName(playerNumber)
        return playerNumber
    return -1

def closeConnection(playerNumber):
    global clients

    if playerNumber in clients:
        connection, address = clients[playerNumber]
        connection.close()
        del clients[playerNumber]
        print(playerNumberToName(playerNumber) + " has been disconnected.")
    else: print("Error: playerNumber does not exist in clients.")  

 

def requestAction(playerNumber):
    global validActions
    sendMessage(playerNumber, "REQUEST: ACTION\n")
    action = getMessage(playerNumber)
    if action in validActions: return action
    else:
        print("Dealer_server: ERROR: Invalid action:", action)
        return ("ERROR: Invalid action: " + str(action))

def requestClose(playerNumber):
    sendMessage(playerNumber, "REQUEST: CLOSE\n")

def updatePlayerBoard(playerNumber, dealerHand, playerHand):
    message = "UPDATE:"
    message += "DEALER:" + dealerHand + ';'
    message += playerNumberToName(playerNumber) + ':' + playerHand + '\n'
    sendMessage(playerNumber, message)
    


#startServer(serverAddress, serverPort)
#acceptConnection()
#sendMessage(0, "Hello there Player 1.")
#requestAction(0)
#getMessage(0)
#closeConnection(0)
#closeServer()
