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
    updateScreen([])

def drawButtons():
    global hit_button
    global stand_button
    global screen
    
    button_width = 120
    button_height = 50
    gap = 20
    center_x = screen.get_width() // 2

    hit_button = pygame.Rect(
        center_x - button_width - gap // 2,
        screen.get_height() - 100,
        button_width,
        button_height
    )

    stand_button = pygame.Rect(
        center_x + gap // 2,
        screen.get_height() - 100,
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

def drawCards(hand):
    global screen
    center_x = screen.get_width() // 2
    center_y = screen.get_height() // 2
    startPos = 350
    
    for card in hand:
        cardImage = pygame.image.load("Images/Cards/" + card + ".png").convert_alpha()
        cardImage = pygame.transform.scale(cardImage, (100, 145))
        #cardRect = cardImage.get_rect(center=(startPos, 350))
        cardRect = cardImage.get_rect(center=(center_x - 50, 350))
        screen.blit(cardImage, cardRect)
        center_x += 100

def closeGameWindow():
    pygame.quit()

def updateScreen(hand):
    global screen
    screen.fill("green")
    drawButtons()
    drawCards(hand)
    pygame.display.flip()

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

#startGameWindow(800, 600, 60)
#getDealerAction()
#time.sleep(4)
#closeGameWindow()
