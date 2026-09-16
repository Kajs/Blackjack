import random
import time

welcomeString = "Welcome to the blackjack table!\n\n"
welcomeString += "The first card letter means D for Diamonds, C for Clubs, H for Hearts and S for Spades, "
welcomeString += "followed by 2-10 for numbered cards, _ACE for Ace, J for Jarl, Q for Queen and K for King.\n"
print(welcomeString)

numDecks = 4
cutCard = 52

print("The shoe contains " + str(numDecks) + " deck(s), for a total of " + str(numDecks*52) + " cards.\n")
print("The cut card is at " + str(cutCard) + " cards. When the shoe reaches or surpasses the cut card, the shoe will either be shuffled or the game will end, at the end of the round.\n")

Cards = ["D_ACE",
         "D2",
         "D3",
         "D4",
         "D5",
         "D6",
         "D7",
         "D8",
         "D9",
         "D10",
         "DJ",
         "DQ",
         "DK",
         "C_ACE",
         "C2",
         "C3",
         "C4",
         "C5",
         "C6",
         "C7",
         "C8",
         "C9",
         "C10",
         "CJ",
         "CQ",
         "CK",
         "H_ACE",
         "H2",
         "H3",
         "H4",
         "H5",
         "H6",
         "H7",
         "H8",
         "H9",
         "H10",
         "HJ",
         "HQ",
         "HK",
         "S_ACE",
         "S2",
         "S3",
         "S4",
         "S5",
         "S6",
         "S7",
         "S8",
         "S9",
         "S10",
         "SJ",
         "SQ",
         "SK",
    ]

def getDeck():
    Deck = []
    for i in range(len(Cards)):
        Deck.append(Cards[i])
    return Deck

def shuffleDeck(d):
    random.shuffle(d)

def drawCard(d):
    card = d[0]
    del d[0]
    return card

def printDeck(d):
    for c in d:
        print(c)

def getCardValue(c):
    if c == "D_ACE" or c == "C_ACE" or c == "H_ACE" or c == "S_ACE":
        return (1, 11)
    if c == "D2" or c == "C2" or c == "H2" or c == "S2":
        return (2, 2)
    if c == "D3" or c == "C3" or c == "H3" or c == "S3":
        return (3, 3)
    if c == "D4" or c == "C4" or c == "H4" or c == "S4":
        return (4, 4)
    if c == "D5" or c == "C5" or c == "H5" or c == "S5":
        return (5, 5)
    if c == "D6" or c == "C6" or c == "H6" or c == "S6":
        return (6, 6)
    if c == "D7" or c == "C7" or c == "H7" or c == "S7":
        return (7, 7)
    if c == "D8" or c == "C8" or c == "H8" or c == "S8":
        return (8, 8)
    if c == "D9" or c == "C9" or c == "H9" or c == "S9":
        return (9, 9)
    if c == "D10" or c == "C10" or c == "H10" or c == "S10":
        return (10, 10)
    if c == "DJ" or c == "CJ" or c == "HJ" or c == "SJ":
        return (10, 10)
    if c == "DQ" or c == "CQ" or c == "HQ" or c == "SQ":
        return (10, 10)
    if c == "DK" or c == "CK" or c == "HK" or c == "SK":
        return (10, 10)
    print("Error: drawCardValue didn't find a match for: " + str(c))
    return None


def resetGame(numDecks):
    newShoe = getDeck()
    shuffleDeck(newShoe)
    while numDecks - 1 > 0:
        additionalDeck = getDeck()
        shuffleDeck(additionalDeck)
        for card in additionalDeck:
            newShoe.append(card)
        numDecks -= 1
    discardPile = []
    dealerHand = []
    playerHand = []
    return (newShoe, discardPile, dealerHand, playerHand)

def dealCards(deck, dealerHand, playerHand): #needs check to see if the deck has enough cards remaining
    for i in range(2):
        playerCard = drawCard(deck)
        playerHand.append(playerCard)
        dealerCard = drawCard(deck)
        dealerHand.append(dealerCard)

def endRound(discardPile, dealerHand, playerHand):
    for i in range(len(playerHand)):
        card = drawCard(playerHand)
        discardPile.append(card)
    for i in range(len(dealerHand)):
        card = drawCard(dealerHand)
        discardPile.append(card)


def getHandTotal(hand):
    numAces = 0
    handTotal = 0

    for card in hand:
        if card == "D_ACE" or card == "C_ACE" or card == "H_ACE" or card == "S_ACE":
            numAces += 1
        (minValue, maxValue) = getCardValue(card)
        handTotal += minValue

    while numAces > 0:
        if handTotal + 10 <= 21:
            handTotal += 10
        numAces -= 1
    return handTotal

def checkForBlackjack(hand):
    return getHandTotal(hand) == 21

def drawAllCards(deck): #for testing purposes
    for i in range(len(deck)):
        card = drawCard(deck)           
        (minValue, maxValue) = getCardValue(card)      
        print("You drew " + card + " with min value " + str(minValue) + " and max value " + str(maxValue))

def takePlayerTurn(deck, playerHand, dealerVisibleCard): #Though meant to be unlikely/impossible, this should probably have some safeguard against an empty deck
    print("PLAYERS turn, press s to stay or h to hit. Dealers card is " + dealerVisibleCard + '.')
    response = ""
    while response != 's':
        handTotal = getHandTotal(playerHand)
        if handTotal > 21:
            print("You may no longer hit, since your hand total exceeds 21.\n")
            time.sleep(1)
            break
        handString = ""
        for card in playerHand:
            handString += card + ' '
        if handTotal == 21:
            print("Your hand is " + handString + "with a total of: " + str(handTotal) + '. BLACKJACK!\n')
            time.sleep(2)
            break
        else:
            print("Your hand is " + handString + "with a total of: " + str(handTotal) + '.')
        response = input()
        if response == 'h':
            card = drawCard(deck)
            print("Your draw is " + card)
            playerHand.append(card)
        if response != 's' and response != 'h':
            print("Invalid input: " + response)

def takeDealerTurn(deck, dealerHand): #Though meant to be unlikely/impossible, this should probably have some safeguard against an empty deck
    print("DEALERS turn, press s to stay or h to hit.")
    response = ""
    while response != 's':
        handTotal = getHandTotal(dealerHand)
        if handTotal > 21:
            print("You may no longer hit, since your hand total exceeds 21.\n")
            time.sleep(1)
            break
        handString = ""
        for card in dealerHand:
            handString += card + ' '
        if handTotal == 21:
            print("Your hand is " + handString + "with a total of: " + str(handTotal) + '. BLACKJACK!\n')
            time.sleep(2)
            break
        else:
            print("Your hand is " + handString + "with a total of: " + str(handTotal) + '.')
            
        response = input()
        if response == 'h':
            card = drawCard(deck)
            print("Your draw is " + card)
            dealerHand.append(card)
        if response != 's' and response != 'h':
            print("Invalid input: " + response)

def declareRoundWinner(dealerHand, playerHand):
    dealerHandTotal = getHandTotal(dealerHand)
    playerHandTotal = getHandTotal(playerHand)

    if playerHandTotal <= 21 and (playerHandTotal > dealerHandTotal or dealerHandTotal > 21):
        print("WINNER________: PLAYER has won this round.")
    elif dealerHandTotal <= 21 and (dealerHandTotal > playerHandTotal or playerHandTotal > 21):
        print("WINNER________: DEALER has won this round.")
    elif playerHandTotal == dealerHandTotal or (playerHandTotal > 21 and dealerHandTotal > 21):
        print("TIE___________: player is tied with dealer this round.")
    time.sleep(2)
    print("Length of shoe is now: " + str(len(newShoe)) + '\n')
            
(newShoe, discardPile, dealerHand, playerHand) = resetGame(numDecks)

while True:   
    while len(newShoe) > cutCard:
        dealCards(newShoe, dealerHand, playerHand)
        takePlayerTurn(newShoe, playerHand, dealerHand[1])
        takeDealerTurn(newShoe, dealerHand)
        declareRoundWinner(dealerHand, playerHand)
        endRound(discardPile, dealerHand, playerHand)
    print("The shoe has reached or passed the cut card. Do you wish to shuffle and play again? Press y to play again or n to end the game.")
    response = input()
    if response == 'n':
        print("Thank you for playing.")
        break
    if response == 'y': (newShoe, discardPile, dealerHand, playerHand) = resetGame(numDecks)
    else: print("Invalid input: " + response)
    
#drawAllCards(newDeck)
#printDeck(newDeck)

