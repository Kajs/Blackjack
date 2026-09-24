from Player_client import *
from Player_gui import *
import multiprocessing

serverAddress = "127.0.0.1"
serverPort = 5000
myPlayerNumber = None
dealerHand = []
myHand = []

def setMyPlayerNumber(playerNumber):  #Store the player number the server has assigned to this client
    global myPlayerNumber
    
    if myPlayerNumber == None:
        myPlayerNumber = int(playerNumber)
        print("I am PLAYER" + str(myPlayerNumber))
    else: print("ERROR in setMyPlayerNumber: player number has already been set.")

def parseMessage(message, guiQueue, actionQueue):  #Handles the actions taken, given what text command the server sends
    global myPlayerNumber
    global dealerHand
    global myHand
    
    commands = message.split("\n")  #split on the '\n' char, which terminates all commands
    for command in commands[:-1]: #skip the last empty command from the last '\n' char
        print("Processing:", command)
        if ':' in command:  #All command types end with ':'
            messageParts = command.split(":", 1)

            messageType = messageParts[0].strip()
            messageValue = messageParts[1].strip()

            #print("Message type:", messageType, "MessageValue", messageValue)

            if messageType == "REQUEST":
                if messageValue == "ACTION":  #This means it's the players turn and the server waits to receive the players action (like hit or stand)
                    print("Your turn.")
                    print("Player_main: putting action request in queue.")
                    guiQueue.put({"type": "REQUEST_ACTION"})         #Tell the gui that it's time to handle clicks on the action buttons
                    print("Player_main: waiting for gui to return action.")
                    action = actionQueue.get()                       #Get the result of any button presses on the gui
                    if action == "HIT": sendMessage("ACTION: HIT")
                    elif action == "STAND": sendMessage("ACTION: STAND")
                    elif action == "QUIT": sendMessage("ACTION: QUIT")
                    else: print("ERROR: invalid action: " + action)
                if messageValue == "CLOSE":  #Sent by the server if the dealer is ending the game, or if the server is ready do disconnect a player, that wants to leave the game
                    guiQueue.put({"type": "CLOSE_GUI"})
                    closeClient()
                    return False
            if messageType == "YOURNUMBERIS": setMyPlayerNumber(messageValue)  #Tell Player_main what number it has been assigned by the server
            if messageType == "UPDATE":             #Parse updates to player/dealer hands and forward them to the gui
                hands = messageValue.split(";")
                for i in range(len(hands)):         #Process all hand contents in the command
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
                    else: print("ERROR in parseMessage: unmatched hand type.")
        else: print("Error in parseMessage: invalid format in message:", str(command))
    return True

def main():  #main game loop on the player side
    startClient(serverAddress, serverPort)
    clientActive = True
    guiQueue = multiprocessing.Queue()
    actionQueue = multiprocessing.Queue()

    guiTitle = "Blackjack - PLAYER1" #preferred set by the server, but due to the servers action request causing a deadlock, it's manual for now, while only one player is supported
    
    guiProcess = multiprocessing.Process(   #start the player gui in it's own process, so it can keep updating when blocking functions are called
        target=startGameWindow,
        args=(guiQueue, actionQueue, 400, 500, 60, guiTitle)   #numbers are width, height and framelimit
    )
    guiProcess.start()

    while clientActive:
        clientActive = parseMessage(getMessage(), guiQueue, actionQueue)

if __name__ == "__main__":
    main()
