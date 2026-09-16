import random

print("Hello World!")
Cards = ["RA",
         "R2",
         "R3",
         "R4",
         "R5",
         "R6",
         "R7",
         "R8",
         "R9",
         "R10",
         "RJ",
         "RQ",
         "RK",
         "KA",
         "K2",
         "K3",
         "K4",
         "K5",
         "K6",
         "K7",
         "K8",
         "K9",
         "K10",
         "KJ",
         "KQ",
         "KK",
         "HA",
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
         "SA",
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
    if c == "RA" or c == "KA" or c == "HA" or c == "SA":
        return (1, 11)
    if c == "R2" or c == "K2" or c == "H2" or c == "S2":
        return (2, 2)
    if c == "R3" or c == "K3" or c == "H3" or c == "S3":
        return (3, 3)
    if c == "R4" or c == "K4" or c == "H4" or c == "S4":
        return (4, 4)
    if c == "R5" or c == "K5" or c == "H5" or c == "S5":
        return (5, 5)
    if c == "R6" or c == "K6" or c == "H6" or c == "S6":
        return (6, 6)
    if c == "R7" or c == "K7" or c == "H7" or c == "S7":
        return (7, 7)
    if c == "R8" or c == "K8" or c == "H8" or c == "S8":
        return (8, 8)
    if c == "R9" or c == "K9" or c == "H9" or c == "S9":
        return (9, 9)
    if c == "R10" or c == "K10" or c == "H10" or c == "S10":
        return (10, 10)
    if c == "RJ" or c == "KJ" or c == "HJ" or c == "SJ":
        return (10, 10)
    if c == "RQ" or c == "KQ" or c == "HQ" or c == "SQ":
        return (10, 10)
    if c == "RK" or c == "KK" or c == "HK" or c == "SK":
        return (10, 10)
    print("Error: drawCardValue didn't find a match for: " + str(c))
    return None


def resetGame():
    newDeck = getDeck()
    #shuffleDeck(newDeck)
    discardPile = []
    dealerHand = []
    playerHand = []
    return (newDeck, discardPile, dealerHand, playerHand)

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

def drawAllCards(deck): #for testing purposes
    for i in range(len(deck)):
        card = drawCard(deck)
        (minValue, maxValue) = getCardValue(card)
        print("You drew " + card + " with min value " + str(minValue) + " and max value " + str(maxValue))       

(newDeck, discardPile, dealerHand, playerHand) = resetGame()
#dealCards(newDeck, dealerHand, playerHand)

#endRound(discardPile, dealerHand, playerHand)
drawAllCards(newDeck)

#printDeck(newDeck)

