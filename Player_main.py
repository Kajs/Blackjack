from Player_client import *
serverAddress = "127.0.0.1"
serverPort = 5000

startClient(serverAddress, serverPort)
clientActive = True
while clientActive:
    clientActive = getMessage()
