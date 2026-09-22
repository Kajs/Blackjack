from Player_client import *
from Player_gui import *
serverAddress = "127.0.0.1"
serverPort = 5000
myPlayerName = None

def setMyPlayerName(playerName):
    global myPlayerName
    
    if myPlayerName == None:
        myPlayerName = playerName
        print("I am " + myPlayerName)
    else: print("ERROR: my player name has already been set.")

def getPlayerTextAction():
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
                print("Your turn. Press s to stand or h to hit.")
                action = getPlayerTextAction()
                if action == "HIT": sendMessage("ACTION: HIT")
                elif action == "STAND": sendMessage("ACTION: STAND")
                else: print("ERROR: invalid action: " + action)
            if messageValue == "CLOSE":
                closeClient()
                return False
        if messageType == "YOURNAMEIS": setMyPlayerName(messageValue)
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
    else: print("Error: invalid format in message:", message)
    return True

#startGameWindow(400, 600, 60)
startClient(serverAddress, serverPort)
clientActive = True
while clientActive:
    clientActive = parseMessage(getMessage())
