from Dealer_game import *
from Dealer_gui import *
import time
    

def takeDealerTurn(deck, dealerHand, playerHand):
    updateScreen(dealerHand, playerHand, False)
    print("DEALERS turn")
    dealerAction = ""
    
    while dealerAction != "stand":
        handInfo = getHandInfo(dealerHand)
        handTotal = getHandTotal(dealerHand)
        if handTotal == 21:            
            print(handInfo + ' BLACKJACK!\n')
            time.sleep(2)
            break
        else: print(handInfo)
        
        dealerAction = getDealerAction()
        if dealerAction == "hit":
            handTotal = takeHitAction(deck, dealerHand)
            updateScreen(dealerHand, playerHand, False)
            if handTotal > 21:
                print("You may no longer hit, since your hand total exceeds 21.\n")
                time.sleep(1)
                break
        if dealerAction == "quit":
            return False
    return True

def takePlayerTurn(deck, playerHand, dealerHand): #Though meant to be unlikely/impossible, this should probably have some safeguard against an empty deck
    updateScreen(dealerHand, playerHand, True)
    dealerVisibleCard = dealerHand[1]
    print("PLAYERS turn, press s to stay or h to hit. Dealers card is " + dealerVisibleCard + '.')
    response = ""
    
    while response != 's':
        handTotal = getHandTotal(playerHand)
        handInfo = getHandInfo(playerHand)
        if handTotal > 21:
            print("You may no longer hit, since your hand total exceeds 21.\n")
            time.sleep(1)
            break
        if handTotal == 21:
            print(handInfo + ' BLACKJACK!\n')
            time.sleep(2)
            break
        else: print(handInfo)
        
        response = input()
        if response == 'h':
            card = drawCard(deck)
            playerHand.append(card)
            updateScreen(dealerHand, playerHand, True)
            print("Your draw is " + card)
        if response != 's' and response != 'h':
            print("Invalid input: " + response)

welcomeString = "Welcome to the blackjack table!\n\n"
welcomeString += "The second card letter means C for Clubs, D for Diamonds, H for Hearts and S for Spades, "
welcomeString += "preceeded by 2-10 for numbered cards, A for Ace, J for Jarl, Q for Queen and K for King.\n"
print(welcomeString)

numDecks = 4
cutCard = 52

print("The shoe contains " + str(numDecks) + " deck(s), for a total of " + str(numDecks*52) + " cards.\n")
print("The cut card is at " + str(cutCard) + " cards. When the shoe reaches or surpasses the cut card, the shoe will either be shuffled or the game will end, at the end of the round.\n")

startGameWindow(800, 600, 60)
            
(shoe, discardPile, dealerHand, playerHand) = resetGame(numDecks)
continuePlaying = True
while continuePlaying:
    while len(shoe) > cutCard and continuePlaying:
        dealCards(shoe, dealerHand, playerHand)
        updateScreen(dealerHand, playerHand, True)
        takePlayerTurn(shoe, playerHand, dealerHand)
        continuePlaying = takeDealerTurn(shoe, dealerHand, playerHand)
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

    
