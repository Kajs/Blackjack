import pygame
import time

hit_button = None
stand_button = None
screen = None

def startGameWindow(width, height, framelimit):
    global screen
    
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    clock.tick(framelimit)
    pygame.font.SysFont("test", 40)    
    
    pygame.display.set_caption("Blackjack")
    updateScreen([], [], True)

def drawButtons():
    global hit_button
    global stand_button
    global screen
    
    button_width = 120
    button_height = 50
    button_displacement = 0.85
    gap = 20
    center_x = screen.get_width() // 2

    hit_button = pygame.Rect(
        center_x - button_width - gap // 2,
        screen.get_height() * button_displacement,
        button_width,
        button_height
    )

    stand_button = pygame.Rect(
        center_x + gap // 2,
        screen.get_height() * button_displacement,
        button_width,
        button_height
    )
    pygame.draw.rect(screen, (100, 100, 100), hit_button)
    pygame.draw.rect(screen, (100, 100, 100), stand_button)

    font = pygame.font.Font(None, 36)
    hit_text = font.render("Hit", True, (255, 255, 255))
    stand_text = font.render("Stand", True, (255, 255, 255))
    screen.blit(hit_text, hit_text.get_rect(center=hit_button.center))
    screen.blit(stand_text, stand_text.get_rect(center=stand_button.center))

def drawCards(dealerHand, playerHand, faceDownMode):
    global screen
    screenWidth = screen.get_width()
    screenHeight = screen.get_height()
    dealerCardWidth = 100
    dealerCardHeight = 145
    dealerCardHDisplacement = 0.65
    playerCardWidth = 100
    playerCardHeight = 145
    playerCardHDisplacement = 0.2
    cardDownscaleFactor = 0.9
    
    while dealerCardWidth * len(dealerHand) > screenWidth:
        dealerCardWidth = dealerCardWidth * cardDownscaleFactor
        dealerCardHeight = dealerCardHeight * cardDownscaleFactor
    while playerCardWidth * len(playerHand) > screenWidth:
        playerCardWidth = playerCardWidth * cardDownscaleFactor
        playerCardHeight = playerCardHeight * cardDownscaleFactor

    center_x = screenWidth // 2
    center_y = screenHeight // 2
    cardWPos = center_x - (dealerCardWidth/2) * (len(dealerHand) - 1)
    cardHPos = screenHeight * dealerCardHDisplacement
    
    for i in range(len(dealerHand)):
        card = ""
        if i == 0 and faceDownMode: card = "FD"
        else: card = dealerHand[i]
        
        cardImage = pygame.image.load("Images/Cards/" + card + ".png").convert_alpha()
        cardImage = pygame.transform.scale(cardImage, (dealerCardWidth, dealerCardHeight))
        cardRect = cardImage.get_rect(center=(cardWPos, cardHPos))
        screen.blit(cardImage, cardRect)
        cardWPos += dealerCardWidth

    cardWPos = center_x - (playerCardWidth/2) * (len(playerHand) - 1)
    cardHPos = screenHeight * playerCardHDisplacement

    for card in playerHand:
        cardImage = pygame.image.load("Images/Cards/" + card + ".png").convert_alpha()
        cardImage = pygame.transform.scale(cardImage, (playerCardWidth, playerCardHeight))
        cardRect = cardImage.get_rect(center=(cardWPos, cardHPos))
        screen.blit(cardImage, cardRect)
        cardWPos += playerCardWidth

def closeGameWindow():
    pygame.quit()

def updateScreen(dealerHand, playerHand, faceDownMode):
    global screen
    screen.fill("green")
    drawButtons()
    drawCards(dealerHand, playerHand, faceDownMode)
    pygame.display.flip()
    pygame.event.pump() #temporary potential fix for pygame not updating. This bug is expected to go away, when the player has a gui and the game continually checks for pygame events during the players turn and this can then be deleted.

def getDealerAction():
    global hit_button
    global stand_button
    
    while True:
        for event in pygame.event.get():
            # Close the window
            if event.type == pygame.QUIT:
                return "quit"

            # Mouse click
            if event.type == pygame.MOUSEBUTTONDOWN:

                if hit_button.collidepoint(event.pos):
                    #print("hit button hit")
                    return "hit"

                if stand_button.collidepoint(event.pos):
                    #print ("stand button hit")
                    return "stand"
