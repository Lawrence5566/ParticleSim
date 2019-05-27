import pygame
pygame.init()

arialFont = pygame.font.SysFont('Arial', 30)
textObj = pygame.font.Font('freesansbold.ttf', 22)
WHITE = 255,255,255
BLACK = 0,0,0
YELLOW = 255,255,0
SILVER = 193,197,201
RED = 255,0,0
BLUE = 0,0,255
width, height = 1000, 600
backgroundColour = 255,255,255
screen = pygame.display.set_mode((width, height))
screen.fill(backgroundColour)

def textBox(centerX,centerY,textObj):       #creates a text box(without the box) 
    TextValue = ""
    while True:
        numbers  = "0123456789"
        letters = "abcdefghijklmnopqrstuvwxyz"
        pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                print(pygame.key.name(event.key)) #for testing
                if pygame.key.name(event.key) in numbers or pygame.key.name(event.key) in letters:
                    screen.fill(backgroundColour)
                    print(pygame.key.name(event.key))
                    TextValue += (pygame.key.name(event.key))
                elif pygame.key.name(event.key) == 'backspace':
                    screen.fill(backgroundColour)
                    print(pygame.key.name(event.key))
                    TextValue = TextValue[:-1]

        Text = textObj.render(TextValue, True, BLACK)
        TextRect = Text.get_rect()
        TextRect.center = (centerX, centerY)
        screen.blit(Text,TextRect)
        pygame.display.flip()

FONT = textObj
textBox(500,300,FONT)
