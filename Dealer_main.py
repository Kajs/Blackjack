from Dealer_game import *
from Dealer_gui import *
from Dealer_server import *
import time
import multiprocessing
serverAddress = "127.0.0.1"
serverPort = 5000

#Handles the overall task of taking the dealers turn by waiting for the dealers action, drawing a card on hit and sending gui updates on changes
def takeDealerTurn(guiQueue, actionQueue, deck, dealerHand, playerHand):
    print("DEALERS turn")
    playerNumber = 1 #temporary, should iterate over each client in Dealer_server and update each
    guiQueue.put({"type": "UPDATE_HAND", "handType": "DEALER", "hand": dealerHand})
    updatePlayerBoard(playerNumber, handToString(dealerHand), handToString(playerHand))
    dealerAction = ""
    continueGame = True     #Used to determine if the dealer wishes to end the game, by pressing the exit button

    while dealerAction != "stand":     #loop until the dealer stands, has a hand that goes above 21 or the dealer has blackjack or 21
        handInfo = getHandInfo(dealerHand)  #Get the hand as text and print it to the terminal
        handTotal = getHandTotal(dealerHand)
        if handTotal == 21:   #Check for blackjack or 21. Skips actions automatically if so
            if len(dealerHand) == 2: print(handInfo + " BLACKJACK!")
            else: print(handInfo + " TWENTY ONE!")
            time.sleep(2)
            break
        else: print(handInfo)

        guiQueue.put({"type": "REQUEST_ACTION"})  #Tell the gui that it's time for the dealer to take an action, by pressing one of the buttons
        dealerAction = actionQueue.get()          #Wait for the dealer to press a button, such as hit or stand

        if dealerAction == "hit":
            handTotal = takeHitAction(deck, dealerHand)     #Draw a card and get the new hand total
            guiQueue.put({"type": "UPDATE_HAND", "handType": "DEALER", "hand": dealerHand})   #Tell the dealer gui to draw the new hand
            updatePlayerBoard(playerNumber, handToString(dealerHand), handToString(playerHand))   #Tell the player gui to draw the new hand
            if handTotal > 21:
                print("You may no longer hit, since your hand total exceeds 21.\n")
                time.sleep(1)
                break
        if dealerAction == "quit":
            if continueGame:
                print("Exit activated - please finish the round and the game will then end. Press exit again, to deactivate.")
                continueGame = False
            else:
                print("Exit deactivated - the game will continue as normal.")
                continueGame = True
    print('')  #Just a newline, to make the terminal output more readable
    return continueGame

#Used to handle the overall task of taking a players turn by sending action requests to the players client and sending updates to the dealer and player gui's, when the players hand changes
def takePlayerTurn(guiQueue, playerNumber, deck, playerHand, dealerHand):
    guiQueue.put({"type": "UPDATE_HAND", "handType": "PLAYER1", "hand": playerHand})
    updatePlayerBoard(playerNumber, handToString(dealerHand), handToString(playerHand)) 
    dealerVisibleCard = dealerHand[1]
    print("PLAYERS turn. Dealers card is " + dealerVisibleCard + '.')
    actionHit = "ACTION: HIT"
    actionStand = "ACTION: STAND"
    actionQuit = "ACTION: QUIT"
    isPlayerActive = True    #Used to determine if a player wishes to quit, at the end of the current round
    
    response = ""
    while response != actionStand:       #loop until the player stands, the hand goes above 21 or the player has blackjack or 21
        handTotal = getHandTotal(playerHand)
        handInfo = getHandInfo(playerHand)
        if handTotal > 21:
            print("You may no longer hit, since your hand total exceeds 21.")
            time.sleep(1)
            break
        if handTotal == 21:
            if len(playerHand) == 2: print(handInfo + " BLACKJACK!")
            else: print(handInfo + " TWENTY ONE!")
            time.sleep(2)
            break
        else: print(handInfo)
        
        response = requestAction(playerNumber)    #server sends an action request to the player client, waits for a response and returns it
        if response == actionHit:
            card = drawCard(deck)
            playerHand.append(card)
            print("Your draw is " + card)
            guiQueue.put({"type": "UPDATE_HAND", "handType": "PLAYER1", "hand": playerHand})    #send the new hand to the dealers gui
            updatePlayerBoard(playerNumber, handToString(dealerHand), handToString(playerHand))    #send the new hand to the players gui
        elif response == actionQuit:
            if isPlayerActive:
                print("Player" + str(playerNumber) + " has activated exit and will be removed, at the end of the round.")
                isPlayerActive = False
            else:
                print("Player" + str(playerNumber) + "has deactivated exit and can continue playing.")
                isPlayerActive = True
        if response != actionStand and response != actionHit and response != actionQuit:
            print("Dealer_main: Invalid action:", response)
    print('') #add a new line, to make the terminal output more clearly separate the end of this players turn and the next player or the dealer
    return isPlayerActive

#Used in combination with a player pressing the exit button and removes them from the game, at the end of the round
def removeExitingPlayers(exitingPlayers, activePlayers):
    for eP in range(len(exitingPlayers)):
        playerNumber = exitingPlayers[eP]
        for aP in range(len(activePlayers)):
            if activePlayers[aP] == playerNumber:
                requestClose(playerNumber)        #send a request to the players client, to close the connection and the gui
                closeConnection(playerNumber)     #closes the connection to the player and removes them from the dictionary of clients
                del activePlayers[aP]
                break    #break since we found a matching player number and there should only be one match
        del exitingPlayers[eP]    

#The main game loop on the dealer side
def main():
    welcomeString = "Welcome to the blackjack table!\n\n"
    welcomeString += "The second card letter means C for Clubs, D for Diamonds, H for Hearts and S for Spades, "
    welcomeString += "preceeded by 2-10 for numbered cards, A for Ace, J for Jarl, Q for Queen and K for King.\n"
    print(welcomeString)

    numDecks = 4
    cutCard = 52

    print("The shoe contains " + str(numDecks) + " deck(s), for a total of " + str(numDecks*52) + " cards.\n")
    print("The cut card is at " + str(cutCard) + " cards. When the shoe reaches or surpasses the cut card, the shoe will either be shuffled or the game will end, at the end of the round.\n")

    guiQueue = multiprocessing.Queue()    #can place input for the dealer gui, such as the contents of a hand or request that an action be taken
    actionQueue = multiprocessing.Queue()   #holds the response from the gui, such as the resulting action taken
    guiProcess = multiprocessing.Process(    #starts the gui in a separate process, so that blocking server calls don't interrupt the gui
        target=startGameWindow,
        args=(guiQueue, actionQueue, 400, 500, 60)     #the numbers are window width, height and framelimit
    )
    guiProcess.start()

    startServer(serverAddress, serverPort)
    newPlayerNumber = acceptConnection()
    activePlayers = []
    exitingPlayers = []
    activePlayers.append(newPlayerNumber)

    (shoe, discardPile, dealerHand, playerHand) = resetGame(numDecks)     #fresh start of the game, with a shuffled shoe of decks and empty card hands
    continuePlaying = True        #turns to false at the end of the dealers turn, if the dealer pressed the exit button
    while continuePlaying:
        while continuePlaying and len(activePlayers) > 0 and len(shoe) > cutCard:
            dealCards(shoe, dealerHand, playerHand)
            dealerFacedownHand = getFacedownHand(dealerHand)
            guiQueue.put({"type": "UPDATE_HAND", "handType": "DEALER", "hand": dealerFacedownHand})   #Send the dealers hand to the dealer gui
            guiQueue.put({"type": "UPDATE_HAND", "handType": "PLAYER1", "hand": playerHand})   #Send player hand to the dealer gui. Should change to the active player, if multiple players are to be supported
            for playerNumber in activePlayers: 
                playerActive = takePlayerTurn(guiQueue, playerNumber, shoe, playerHand, dealerFacedownHand)  
                if not playerActive: exitingPlayers.append(playerNumber)  
            continuePlaying = takeDealerTurn(guiQueue, actionQueue, shoe, dealerHand, playerHand)
            declareRoundWinner(dealerHand, playerHand)
            print("Length of shoe is now: " + str(len(shoe)) + '\n')    #The shoe is not drawn in gui, but this allows the number of remaining cards to be read in the terminal
            endRound(discardPile, dealerHand, playerHand)               #move all hand cards to the discard pile
            removeExitingPlayers(exitingPlayers, activePlayers)

        if continuePlaying and len(activePlayers) > 0:     #ask to shuffle the shoe or end the game, once the cut card is reached
            print("The shoe has reached or passed the cut card. Do you wish to shuffle and play again? Press y to play again or n to end the game.")
            response = input()
            if response == 'n': break
            if response == 'y': (shoe, discardPile, dealerHand, playerHand) = resetGame(numDecks)
            else: print("Invalid input: " + response)
        if len(activePlayers) == 0:
            print("All active players have exited - ending game.")
            break
    print("Thank you for playing.")
    guiQueue.put({"type": "CLOSE_GUI"})
    for playerNumber in activePlayers:   #close remaining player connections and gui's
        requestClose(playerNumber)
        closeConnection(playerNumber)
    closeServer()

if __name__ == "__main__":
    main()