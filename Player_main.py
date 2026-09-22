from Player_client import *
from Player_gui import *
serverAddress = "127.0.0.1"
serverPort = 5000

#startGameWindow(400, 600, 60)
startClient(serverAddress, serverPort)
clientActive = True
while clientActive:
    clientActive = getMessage()
