import pygame
import time
import traceback
from queue import Empty

hit_button = None
stand_button = None
exit_button = None
screen = None
loadedImages = {}
dealerHand = []
myHand = []

#Starts the player gui and continually draws the gui and parses commands from the guiQueue. Responses are put in actionQueue, that Player_main can send to the server
def startGameWindow(guiQueue, actionQueue, width, height, framelimit, title):
    global screen
    global dealerHand
    global myHand
    print("PLAYER GUI PROCESS STARTED")
    
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    clock.tick(framelimit)   
    
    pygame.display.set_caption(title)
    updateScreen(dealerHand, myHand)

    running = True
    while running:
        try:
            #print("Trying to fetch gui message") 
            message = guiQueue.get_nowait()
            print("Gui message received:", message["type"]) 
            if message["type"] == "REQUEST_ACTION":
                print("Gui: getting player action.") 
                action = getPlayerAction(dealerHand, myHand)
                actionQueue.put(action)
            elif message["type"] == "UPDATE_HAND":
                handType = message["handType"]
                hand = message["hand"]
                if handType == "DEALER":
                    dealerHand = hand
                elif handType == "MYHAND":
                    myHand = hand
                else: print("Player_gui: unmatched hand type.")
            elif message["type"] == "CLOSE_GUI": 
                closeGameWindow()
                break
            else: print("Player_gui: unmatched message:", message)
        except Empty: pass
        updateScreen(dealerHand, myHand)

def drawButtons():  #Handles drawing of the hit, stand and exit buttons
    global hit_button
    global stand_button
    global exit_button
    global screen
    
    button_width = 120
    button_height = 50
    button_displacement = 0.85  #used to place the hit and stand buttons, displaced at a fixed percentage of the total window height
    gap = 20
    center_x = screen.get_width() // 2   #used to place buttons in relation to the center of the window

    hit_button = pygame.Rect(  #The hit button, which is placed in the lower 15% of the window, to the left of the center
        center_x - button_width - gap // 2,
        screen.get_height() * button_displacement,
        button_width,
        button_height
    )

    stand_button = pygame.Rect(  #The stand button, which is placed in the lower 15% of the window, to the right of the center
        center_x + gap // 2,
        screen.get_height() * button_displacement,
        button_width,
        button_height
    )

    exit_button = pygame.Rect(   #The exit button, which is placed in the upper right corner
        screen.get_width() - button_width/2,
        0,
        button_width/2,
        button_height/2
    )

    pygame.draw.rect(screen, (100, 100, 100), hit_button)  #Draw the button rectangles
    pygame.draw.rect(screen, (100, 100, 100), stand_button)
    pygame.draw.rect(screen, (200, 000, 000), exit_button)

    font = pygame.font.Font(None, 36)
    hit_text = font.render("Hit", True, (255, 255, 255))
    stand_text = font.render("Stand", True, (255, 255, 255))
    exit_text = font.render("Exit", True, (255, 255, 255))
    screen.blit(hit_text, hit_text.get_rect(center=hit_button.center))  #Place the hit/stand/exit text on the corresponding buttons
    screen.blit(stand_text, stand_text.get_rect(center=stand_button.center))
    screen.blit(exit_text, exit_text.get_rect(center=exit_button.center))
    
def drawCards(dealerHand, playerHand):  #Handles the drawing of cards in the player and dealers hand
    global screen
    global loadedImages
    
    screenWidth = screen.get_width()
    screenHeight = screen.get_height()
    dealerCardWidth = 100
    dealerCardHeight = 145
    dealerCardHDisplacement = 0.2    #Used to place the dealers card 20% away from the top of the window
    playerCardWidth = 100
    playerCardHeight = 145
    playerCardHDisplacement = 0.65   #Used to place the players cards 35% away from the bottom of the window
    cardDownscaleFactor = 0.9   #Used to downscale cards, in case they would not otherwise fit on the screen
    

    while dealerCardWidth * len(dealerHand) > screenWidth:  #Check if the total width of cards in a hand can fit on the screen and if not, downscale them until they can
        dealerCardWidth = dealerCardWidth * cardDownscaleFactor
        dealerCardHeight = dealerCardHeight * cardDownscaleFactor
    while playerCardWidth * len(playerHand) > screenWidth:
        playerCardWidth = playerCardWidth * cardDownscaleFactor
        playerCardHeight = playerCardHeight * cardDownscaleFactor

    center_x = screenWidth // 2
    center_y = screenHeight // 2
    cardWPos = center_x - (playerCardWidth/2) * (len(playerHand) - 1)   #calculate the starting horizontal position of the first card in the hand
    cardHPos = screenHeight * playerCardHDisplacement
    
    for card in playerHand:
        cardImage = None
        
        if card in loadedImages: cardImage = loadedImages[card]  #if the image was loaded previously, get the stored version
        else:
            cardImage = pygame.image.load("Images/Cards/" + card + ".png").convert_alpha()
            loadedImages[card] = cardImage
        cardImage = pygame.transform.scale(cardImage, (playerCardWidth, playerCardHeight))   #set the desired size, based on the original size and the extent to which they have been downscaled
        cardRect = cardImage.get_rect(center=(cardWPos, cardHPos))
        screen.blit(cardImage, cardRect)
        cardWPos += playerCardWidth  #shift the horizontal position one card length to the right for the next card in the hand

    cardWPos = center_x - (dealerCardWidth/2) * (len(dealerHand) - 1)
    cardHPos = screenHeight * dealerCardHDisplacement

    for card in dealerHand:  #Start placing the dealer cards. Aside from the vertical position, this is idential to how the player cards were placed and drawn
        cardImage = None
        
        if card in loadedImages: cardImage = loadedImages[card]
        else:
            cardImage = pygame.image.load("Images/Cards/" + card + ".png").convert_alpha()
            loadedImages[card] = cardImage
        cardImage = pygame.transform.scale(cardImage, (dealerCardWidth, dealerCardHeight))
        cardRect = cardImage.get_rect(center=(cardWPos, cardHPos))
        screen.blit(cardImage, cardRect)
        cardWPos += dealerCardWidth

def closeGameWindow():
    print("Closing player gui.")
    pygame.quit()

def updateScreen(dealerHand, playerHand):  #Responsible for drawing the entire gui and calls all the related sub functions
    global screen
    pygame.event.pump()

    screen.fill("green")
    drawButtons()
    drawCards(dealerHand, playerHand)
    pygame.display.flip()

def getPlayerAction(dealerHand, playerHand):  #Used when it is the players turn to take an action and handles button clicks
    global hit_button
    global stand_button
    global exit_button
    
    pygame.event.clear(pygame.MOUSEBUTTONDOWN)  #clear mouse events, in case any were on the hit or stand buttons, during previous turns
    while True:
        updateScreen(dealerHand, playerHand)
        for event in pygame.event.get():
            # Close the window
            if event.type == pygame.QUIT:
                return "QUIT"

            # Mouse click
            if event.type == pygame.MOUSEBUTTONDOWN:

                if hit_button.collidepoint(event.pos):
                    return "HIT"

                if stand_button.collidepoint(event.pos):
                    return "STAND"
                
                if exit_button.collidepoint(event.pos):
                    print ("exit button hit")
                    return "QUIT"