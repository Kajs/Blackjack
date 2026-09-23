from Player_client import *
from Player_gui import *
serverAddress = "127.0.0.1"
serverPort = 5000
myPlayerName = None
dealerHand = []
myHand = []

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
    global dealerHand
    global myHand
    
    commands = message.split("\n")
    for command in commands[:-1]: #skip the last empty command
        print("Processing:", command)
        if ':' in command:
            messageParts = command.split(":", 1)

            messageType = messageParts[0].strip()
            messageValue = messageParts[1].strip()

            #print("Message type:", messageType, "MessageValue", messageValue)

            if messageType == "REQUEST":
                if messageValue == "ACTION":
                    print("Your turn. Press s to stand or h to hit.")
                    action = getPlayerAction(dealerHand, myHand)
                    if action == "HIT": sendMessage("ACTION: HIT")
                    elif action == "STAND": sendMessage("ACTION: STAND")
                    else: print("ERROR: invalid action: " + action)
                if messageValue == "CLOSE":
                    closeClient()
                    return False
            if messageType == "YOURNAMEIS": setMyPlayerName(messageValue)
            if messageType == "UPDATE":
                hands = messageValue.split(";")
                for i in range(len(hands)):
                    handString = hands[i]
                    handParts = handString.split(':', 1)
                    handType = handParts[0].strip()

                    cardParts = handParts[1].strip()
                    cards = cardParts.split(',')
                    cardString = ""

                    for i in range(len(cards)):
                        cardString += cards[i]
                        if i < len(cards) - 1:
                            cardString += " "

                    if handType == "DEALER":
                        print("Dealer hand: " + cardString)
                        dealerHand = cards
                        updateScreen(dealerHand, myHand)
                    elif handType == myPlayerName:
                        print("My hand: " + cardString)
                        myHand = cards
                        updateScreen(dealerHand, myHand)
                    else: print("ERROR parsing hand")
        else: print("Error: invalid format in message:", str(command))
    return True

startClient(serverAddress, serverPort)
clientActive = True
parseMessage(getMessage()) # Wait to receive player name, before starting gui
startGameWindow(400, 500, 60, "Blackjack - " + myPlayerName)
while clientActive:
    clientActive = parseMessage(getMessage())
