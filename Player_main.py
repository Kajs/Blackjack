from Player_client import *
from Player_gui import *
import multiprocessing

serverAddress = "127.0.0.1"
serverPort = 5000
myPlayerNumber = None
dealerHand = []
myHand = []

#Store the player name the server has
def setMyPlayerNumber(playerNumber):
    global myPlayerNumber
    
    if myPlayerNumber == None:
        myPlayerNumber = int(playerNumber)
        print("I am PLAYER" + str(myPlayerNumber))
    else: print("ERROR in setMyPlayerNumber: player number has already been set.")

def parseMessage(message, guiQueue, actionQueue):
    global myPlayerNumber
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
                    print("Your turn.")
                    print("Player_main: putting action request in queue.")
                    guiQueue.put({"type": "REQUEST_ACTION"})
                    print("Player_main: waiting for gui to return action.")
                    action = actionQueue.get()
                    if action == "HIT": sendMessage("ACTION: HIT")
                    elif action == "STAND": sendMessage("ACTION: STAND")
                    elif action == "QUIT": sendMessage("ACTION: QUIT")
                    else: print("ERROR: invalid action: " + action)
                if messageValue == "CLOSE":
                    guiQueue.put({"type": "CLOSE_GUI"})
                    closeClient()
                    return False
            if messageType == "YOURNUMBERIS": setMyPlayerNumber(messageValue)
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
                        guiQueue.put({"type": "UPDATE_HAND", "handType": "DEALER", "hand": dealerHand})
                    elif handType == "PLAYER" + str(myPlayerNumber):
                        print("My hand: " + cardString)
                        myHand = cards
                        guiQueue.put({"type": "UPDATE_HAND", "handType": "MYHAND", "hand": myHand})
                    else: print("ERROR parsing hand")
        else: print("Error: invalid format in message:", str(command))
    return True

def main():
    startClient(serverAddress, serverPort)
    clientActive = True
    guiQueue = multiprocessing.Queue()
    actionQueue = multiprocessing.Queue()

    guiTitle = "Blackjack - PLAYER1" #preferred set by the server, but due to causing a deadlock from the servers action request, it's manual while only one player is supported
    
    guiProcess = multiprocessing.Process(
        target=startGameWindow,
        args=(guiQueue, actionQueue, 400, 500, 60, guiTitle)
    )
    guiProcess.start()

    while clientActive:
        clientActive = parseMessage(getMessage(), guiQueue, actionQueue)

if __name__ == "__main__":
    main()
