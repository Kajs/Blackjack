import pygame
import time

hit_button = None
stand_button = None
exit_button = None
screen = None
loadedImages = {}

def startGameWindow(width, height, framelimit):
    global screen
    
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    clock.tick(framelimit)   
    
    pygame.display.set_caption("Blackjack")
    updateScreen([], [], True)

def drawButtons():
    global hit_button
    global stand_button
    global exit_button
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

    exit_button = pygame.Rect(
        screen.get_width() - button_width/2,
        0,
        button_width/2,
        button_height/2
    )

    pygame.draw.rect(screen, (100, 100, 100), hit_button)
    pygame.draw.rect(screen, (100, 100, 100), stand_button)
    pygame.draw.rect(screen, (200, 000, 000), exit_button)

    font = pygame.font.Font(None, 36)
    hit_text = font.render("Hit", True, (255, 255, 255))
    stand_text = font.render("Stand", True, (255, 255, 255))
    exit_text = font.render("Exit", True, (255, 255, 255))
    screen.blit(hit_text, hit_text.get_rect(center=hit_button.center))
    screen.blit(stand_text, stand_text.get_rect(center=stand_button.center))
    screen.blit(exit_text, exit_text.get_rect(center=exit_button.center))
    
def drawCards(dealerHand, playerHand):
    global screen
    global loadedImages
    
    screenWidth = screen.get_width()
    screenHeight = screen.get_height()
    dealerCardWidth = 100
    dealerCardHeight = 145
    dealerCardHDisplacement = 0.2
    playerCardWidth = 100
    playerCardHeight = 145
    playerCardHDisplacement = 0.65
    cardDownscaleFactor = 0.9
    
    while dealerCardWidth * len(dealerHand) > screenWidth:
        dealerCardWidth = dealerCardWidth * cardDownscaleFactor
        dealerCardHeight = dealerCardHeight * cardDownscaleFactor
    while playerCardWidth * len(playerHand) > screenWidth:
        playerCardWidth = playerCardWidth * cardDownscaleFactor
        playerCardHeight = playerCardHeight * cardDownscaleFactor

    center_x = screenWidth // 2
    center_y = screenHeight // 2
    cardWPos = center_x - (playerCardWidth/2) * (len(playerHand) - 1)
    cardHPos = screenHeight * playerCardHDisplacement
    
    for i in range(len(playerHand)):
        card = playerHand[i]
        cardImage = None
        
        if card in loadedImages: cardImage = loadedImages[card]
        else:
            cardImage = pygame.image.load("Images/Cards/" + card + ".png").convert_alpha()
            loadedImages[card] = cardImage
        cardImage = pygame.transform.scale(cardImage, (playerCardWidth, playerCardHeight))
        cardRect = cardImage.get_rect(center=(cardWPos, cardHPos))
        screen.blit(cardImage, cardRect)
        cardWPos += playerCardWidth

    cardWPos = center_x - (dealerCardWidth/2) * (len(dealerHand) - 1)
    cardHPos = screenHeight * dealerCardHDisplacement

    for i in range(len(dealerHand)):
        card = dealerHand[i]
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
    pygame.quit()

def updateScreen(dealerHand, playerHand, faceDownMode):
    global screen
    screen.fill("green")
    drawButtons()
    drawCards(dealerHand, playerHand, faceDownMode)
    pygame.display.flip()

def getDealerAction():
    global hit_button
    global stand_button
    global exit_button
    
    while True:
        for event in pygame.event.get():
            # Close the window
            if event.type == pygame.QUIT:
                return "quit"

            # Mouse click
            if event.type == pygame.MOUSEBUTTONDOWN:

                if hit_button.collidepoint(event.pos):
                    return "hit"

                if stand_button.collidepoint(event.pos):
                    return "stand"
                
                if exit_button.collidepoint(event.pos):
                    print ("exit button hit")
                    return "quit"
    
