import socket

serverAddress = "127.0.0.1"
serverPort = 5000
serverSocket = None
clients = []
validActions = ["ACTION: HIT", "ACTION: STAND"]
playerNumber = 0

def getPlayerName(playerNumber):
    playerName = "Player " + str(playerNumber)
    return playerName

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
        print(getPlayerName(playerNumber) + " connected:", address, '\n')
        clients.append((playerNumber, connection, address))

def closeConnection(playerIndex):
    global clients
    numClients = len(clients)

    if playerIndex < numClients:
        playerNumber, connection, address = clients[playerIndex]
        connection.close()
        print(getPlayerName(playerNumber) + " has been disconnected.")
    else: print("Error: playerIndex exceeds number of clients.")

def getMessage(playerIndex):
    global serverSocket
    global clients
    numClients = len(clients)  

    if playerIndex < numClients:
        playerNumber, connection, address = clients[playerIndex]
        message = connection.recv(1024)
        decodedMessage = message.decode()
        #print(getPlayerName(playerNumber) + " says:", decodedMessage)
        return decodedMessage
    else: print("Error: playerIndex exceeds number of clients.")        

def sendMessage(playerIndex, message):
    global clients
    numClients = len(clients)

    if playerIndex < numClients:
        playerNumber, connection, address = clients[playerIndex]
        connection.sendall(message.encode())
    else: print("Error: playerIndex exceeds number of clients.")

def requestAction(playerIndex):
    global validActions
    sendMessage(playerIndex, "REQUEST: ACTION")
    action = getMessage(playerIndex)
    if action in validActions: return action
    else:
        print("ERROR: Invalid action: " + action)
        return ("ERROR: Invalid action: " + action)

def requestClose(playerIndex):
    sendMessage(playerIndex, "REQUEST: CLOSE")


#startServer(serverAddress, serverPort)
#acceptConnection()
#sendMessage(0, "Hello there Player 1.")
#requestAction(0)
#getMessage(0)
#closeConnection(0)
#closeServer()
