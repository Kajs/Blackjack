import random
import time

Cards = ["AC",
         "2C",
         "3C",
         "4C",
         "5C",
         "6C",
         "7C",
         "8C",
         "9C",
         "10C",
         "JC",
         "QC",
         "KC",
         "AD",
         "2D",
         "3D",
         "4D",
         "5D",
         "6D",
         "7D",
         "8D",
         "9D",
         "10D",
         "JD",
         "QD",
         "KD",
         "AH",
         "2H",
         "3H",
         "4H",
         "5H",
         "6H",
         "7H",
         "8H",
         "9H",
         "10H",
         "JH",
         "QH",
         "KH",
         "AS",
         "2S",
         "3S",
         "4S",
         "5S",
         "6S",
         "7S",
         "8S",
         "9S",
         "10S",
         "JS",
         "QS",
         "KS",
    ]

#Returns a list with all the cards definced in the Cards list
def getDeck():
    Deck = []
    for i in range(len(Cards)):
        Deck.append(Cards[i])
    return Deck

def shuffleDeck(d):
    random.shuffle(d)

#Used for drawing a card from a deck (or multiple decks in sequence) of cards. The card is deleted, to simulate it no longer being in the deck
def drawCard(d):
    card = d[0]
    del d[0]
    return card

#Returns the numerical value of a card for blackjack. Minimum and maximum is the same for all cards, except aces
def getCardValue(c):
    if c == "AC" or c == "AD" or c == "AH" or c == "AS":
        return (1, 11)
    if c == "2C" or c == "2D" or c == "2H" or c == "2S":
        return (2, 2)
    if c == "3C" or c == "3D" or c == "3H" or c == "3S":
        return (3, 3)
    if c == "4C" or c == "4D" or c == "4H" or c == "4S":
        return (4, 4)
    if c == "5C" or c == "5D" or c == "5H" or c == "5S":
        return (5, 5)
    if c == "6C" or c == "6D" or c == "6H" or c == "6S":
        return (6, 6)
    if c == "7C" or c == "7D" or c == "7H" or c == "7S":
        return (7, 7)
    if c == "8C" or c == "8D" or c == "8H" or c == "8S":
        return (8, 8)
    if c == "9C" or c == "9D" or c == "9H" or c == "9S":
        return (9, 9)
    if c == "10C" or c == "10D" or c == "10H" or c == "10S":
        return (10, 10)
    if c == "JC" or c == "JD" or c == "JH" or c == "JS":
        return (10, 10)
    if c == "QC" or c == "QD" or c == "QH" or c == "QS":
        return (10, 10)
    if c == "KC" or c == "KD" or c == "KH" or c == "KS":
        return (10, 10)
    print("Error: getCardValue didn't find a match for: " + str(c))
    return None

#Gives a string representation of the cards in a players/dealers hand, along with it's effective value (aces may count as 1's, if 11 would put it above 21)
def getHandInfo(hand):
    handString = ""
    for card in hand:
        handString += card + ' '
    return ("Your hand is " + handString + "with a total of: " + str(getHandTotal(hand)) + '.')

#Gives a comma separated string representation of a hand of cards. Used when the server needs to send hand updates to player gui's
def handToString(hand):
    handString = ""
    numCards = len(hand)
    for i in range(numCards):
        handString += hand[i]
        if i < numCards - 1:
            handString += ','
    return handString

#Used to get a copy of a hand, where the first card is facedown, so players can't see which one it is
def getFacedownHand(hand):
    fdHand = ["FD"]
    fdHand.append(hand[1])
    return fdHand

#Returns a sequence of shuffled decks as a single list, as well as empty lists for the discard pile, player hand and dealer hand. Used at the start of a game or to reshuffle the decks, when the cut card is reached
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

#Deal a hand of 2 cards for the dealer and a player
def dealCards(deck, dealerHand, playerHand):
    for i in range(2):
        playerCard = drawCard(deck)
        playerHand.append(playerCard)
        dealerCard = drawCard(deck)
        dealerHand.append(dealerCard)

#Moves all cards in a dealer hand and player hand to the discard pile, to prepare for the next round
def endRound(discardPile, dealerHand, playerHand):
    for i in range(len(playerHand)):
        card = drawCard(playerHand)
        discardPile.append(card)
    for i in range(len(dealerHand)):
        card = drawCard(dealerHand)
        discardPile.append(card)

#Returns the effective numerical total of a hand of cards, with aces counting as 1's, if their max of 11 would put the hand above or further above 21
def getHandTotal(hand):
    numAces = 0
    handTotal = 0

    for card in hand:
        if card == "AC" or card == "AD" or card == "AH" or card == "AS":
            numAces += 1
        (minValue, maxValue) = getCardValue(card)
        handTotal += minValue

    while numAces > 0:
        if handTotal + 10 <= 21:
            handTotal += 10
        numAces -= 1
    return handTotal

#Removes a card from the shoe and adds it to the hand
def takeHitAction(deck, hand):
    card = drawCard(deck)
    print("Card draw is " + card)
    hand.append(card)
    return getHandTotal(hand)

def declareRoundWinner(dealerHand, playerHand):
    dealerHandTotal = getHandTotal(dealerHand)
    playerHandTotal = getHandTotal(playerHand)

    if playerHandTotal == 21 and len(playerHand) == 2 and dealerHandTotal == 21 and len(dealerHand) > 2: #Blackjack vs 21
        print("WINNER________: PLAYER has won this round.")
    elif dealerHandTotal == 21 and len(dealerHand) == 2 and playerHandTotal == 21 and len(playerHand) > 2: #Blackjack vs 21
        print("WINNER________: DEALER has won this round.")
    elif playerHandTotal <= 21 and (playerHandTotal > dealerHandTotal or dealerHandTotal > 21):
        print("WINNER________: PLAYER has won this round.")
    elif dealerHandTotal <= 21 and (dealerHandTotal > playerHandTotal or playerHandTotal > 21):
        print("WINNER________: DEALER has won this round.")
    elif playerHandTotal == dealerHandTotal or (playerHandTotal > 21 and dealerHandTotal > 21):
        print("TIE___________: player is tied with dealer this round.")
    time.sleep(2)

