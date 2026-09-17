from Dealer_game import *
from Dealer_gui import *
import time

def printHand(hand):
    handString = ""
    for card in hand:
        handString += card + ' '
    print("Your hand is " + handString + "with a total of: " + str(getHandTotal(hand)) + '.')
    

def takeDealerTurn(deck, hand):
    print("DEALERS turn")
    dealerAction = ""
    while dealerAction != "stand":
        printHand(hand)
        dealerAction = getDealerAction()
        if dealerAction == "hit":
            handTotal = takeHitAction(deck, hand)
            updateScreen(hand)
            if handTotal > 21:
                break

welcomeString = "Welcome to the blackjack table!\n\n"
welcomeString += "The first card letter means D for Diamonds, C for Clubs, H for Hearts and S for Spades, "
welcomeString += "followed by 2-10 for numbered cards, _ACE for Ace, J for Jarl, Q for Queen and K for King.\n"
print(welcomeString)

numDecks = 4
cutCard = 52

print("The shoe contains " + str(numDecks) + " deck(s), for a total of " + str(numDecks*52) + " cards.\n")
print("The cut card is at " + str(cutCard) + " cards. When the shoe reaches or surpasses the cut card, the shoe will either be shuffled or the game will end, at the end of the round.\n")

startGameWindow(600, 600, 60)
            
(shoe, discardPile, dealerHand, playerHand) = resetGame(numDecks)

while True:
    while len(shoe) > cutCard:
        dealCards(shoe, dealerHand, playerHand)
        updateScreen(dealerHand)
        takePlayerTurn(shoe, playerHand, dealerHand[1])
        takeDealerTurn(shoe, dealerHand)
        declareRoundWinner(dealerHand, playerHand)
        print("Length of shoe is now: " + str(len(shoe)) + '\n')
        endRound(discardPile, dealerHand, playerHand)
    print("The shoe has reached or passed the cut card. Do you wish to shuffle and play again? Press y to play again or n to end the game.")
    response = input()
    if response == 'n':
        print("Thank you for playing.")
        break
    if response == 'y': (shoe, discardPile, dealerHand, playerHand) = resetGame(numDecks)
    else: print("Invalid input: " + response)


    
