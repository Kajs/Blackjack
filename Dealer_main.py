from Dealer_game import *
from Dealer_gui import *
from Dealer_server import *
import time
import multiprocessing
serverAddress = "127.0.0.1"
serverPort = 5000

def takeDealerTurn(guiQueue, actionQueue, deck, dealerHand, playerHand):
    print("DEALERS turn")
    playerNumber = 1 #temporary, should iterate over each client in Dealer_server and update each
    guiQueue.put({"type": "UPDATE_HAND", "handType": "DEALER", "hand": dealerHand}) #updateScreen(dealerHand, playerHand, False)
    updatePlayerBoard(playerNumber, handToString(dealerHand), handToString(playerHand))
    dealerAction = ""
    
    while dealerAction != "stand":
        handInfo = getHandInfo(dealerHand)
        handTotal = getHandTotal(dealerHand)
        if handTotal == 21:
            if len(dealerHand) == 2: print(handInfo + " BLACKJACK!")
            else: print(handInfo + " TWENTY ONE!")
            time.sleep(2)
            break
        else: print(handInfo)
        
        #dealerAction = getDealerAction(dealerHand, playerHand)
        guiQueue.put({"type": "REQUEST_ACTION"})
        dealerAction = actionQueue.get()

        if dealerAction == "hit":
            handTotal = takeHitAction(deck, dealerHand)
            guiQueue.put({"type": "UPDATE_HAND", "handType": "DEALER", "hand": dealerHand}) #updateScreen(dealerHand, playerHand, False)
            updatePlayerBoard(playerNumber, handToString(dealerHand), handToString(playerHand))
            if handTotal > 21:
                print("You may no longer hit, since your hand total exceeds 21.\n")
                time.sleep(1)
                break
        if dealerAction == "quit":
            return False
    print('')
    return True

def takePlayerTurn(guiQueue, playerNumber, deck, playerHand, dealerHand): #Though meant to be unlikely/impossible, this should probably have some safeguard against an empty deck
    guiQueue.put({"type": "UPDATE_HAND", "handType": "PLAYER1", "hand": playerHand})#updateScreen(dealerHand, playerHand, True)
    updatePlayerBoard(playerNumber, handToString(dealerHand), handToString(playerHand)) 
    dealerVisibleCard = dealerHand[1]
    print("PLAYERS turn, press s to stand or h to hit. Dealers card is " + dealerVisibleCard + '.')
    actionHit = "ACTION: HIT"
    actionStand = "ACTION: STAND"
    
    response = ""
    while response != actionStand:
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
        
        response = requestAction(playerNumber)
        if response == actionHit:
            card = drawCard(deck)
            playerHand.append(card)
            print("Your draw is " + card)
            guiQueue.put({"type": "UPDATE_HAND", "handType": "PLAYER1", "hand": playerHand}) #updateScreen(dealerHand, playerHand, True)
            updatePlayerBoard(playerNumber, handToString(dealerHand), handToString(playerHand))
        if response != actionStand and response != actionHit:
            print("Invalid action: " + response)
    print('')

def main():
    welcomeString = "Welcome to the blackjack table!\n\n"
    welcomeString += "The second card letter means C for Clubs, D for Diamonds, H for Hearts and S for Spades, "
    welcomeString += "preceeded by 2-10 for numbered cards, A for Ace, J for Jarl, Q for Queen and K for King.\n"
    print(welcomeString)

    numDecks = 4
    cutCard = 52

    print("The shoe contains " + str(numDecks) + " deck(s), for a total of " + str(numDecks*52) + " cards.\n")
    print("The cut card is at " + str(cutCard) + " cards. When the shoe reaches or surpasses the cut card, the shoe will either be shuffled or the game will end, at the end of the round.\n")

    guiQueue = multiprocessing.Queue()
    actionQueue = multiprocessing.Queue()
    guiProcess = multiprocessing.Process(
        target=startGameWindow,
        args=(guiQueue, actionQueue, 400, 500, 60)
    )
    guiProcess.start()
    #startGameWindow(400, 500, 60)

    startServer(serverAddress, serverPort)
    acceptConnection()

    playerNumber = 1
    (shoe, discardPile, dealerHand, playerHand) = resetGame(numDecks)
    continuePlaying = True
    while continuePlaying:
        while len(shoe) > cutCard and continuePlaying:
            dealCards(shoe, dealerHand, playerHand)
            dealerFacedownHand = getFacedownHand(dealerHand)
            guiQueue.put({"type": "UPDATE_HAND", "handType": "DEALER", "hand": dealerFacedownHand})
            guiQueue.put({"type": "UPDATE_HAND", "handType": "PLAYER1", "hand": playerHand})#updateScreen(dealerHand, playerHand, True)
            takePlayerTurn(guiQueue, playerNumber, shoe, playerHand, dealerFacedownHand)      
            continuePlaying = takeDealerTurn(guiQueue, actionQueue, shoe, dealerHand, playerHand)
            declareRoundWinner(dealerHand, playerHand)
            print("Length of shoe is now: " + str(len(shoe)) + '\n')
            endRound(discardPile, dealerHand, playerHand)
        if continuePlaying:
            print("The shoe has reached or passed the cut card. Do you wish to shuffle and play again? Press y to play again or n to end the game.")
            response = input()
            if response == 'n': break
            if response == 'y': (shoe, discardPile, dealerHand, playerHand) = resetGame(numDecks)
            else: print("Invalid input: " + response)
    print("Thank you for playing.")
    closeGameWindow()
    requestClose(playerNumber)
    closeConnection(playerNumber)
    closeServer()

if __name__ == "__main__":
    main()