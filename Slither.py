import pygame
import random

pygame.init()
pygame.font.init()
pygame.mixer.init()

WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (0,0,255)
RED = (255,0,0)
GREEN = (0,155,0)
YELLOW = (255,255,0)

WIDTH, HEIGHT = 800, 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Slither")

icon = pygame.image.load('Assets\Apple.png')
pygame.display.set_icon(icon)

headofsnake = pygame.image.load('Assets\snakehead.png')
appleimg = pygame.image.load('Assets\Apple.png')


direction = "right"

BLOCK_SIZE = 15

APPLE_SIZE = 25

FPS = 30
clock = pygame.time.Clock()

smallfont = pygame.font.SysFont('comicsansms', 25)
medfont = pygame.font.SysFont('comicsansms', 50)
medfont_4_gameover = pygame.font.SysFont('comicsansms', 37)
largefont = pygame.font.SysFont('comicsansms', 80)

#Sound Effect for snake eating sound and other...

Yummi = pygame.mixer.Sound('Assets\eat.mp3')

def pause():

    pause = True
    message('Paused', RED, -100, size = 'large')
    message('Press C to continue or Q to quit', BLACK, 25,'medium')

    pygame.display.update()
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    pause = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    

        clock.tick(FPS)
        
def score(score):
    text = smallfont.render("Score: " + str(score), True, BLACK)
    screen.blit(text, [0,0])

def randAppleGen():
    randAppleX = round(random.randrange(0, WIDTH - APPLE_SIZE)/25.0)*25.0
    randAppleY = round(random.randrange(0, HEIGHT - APPLE_SIZE)/25.0)*25.0

    return randAppleX, randAppleY

randAppleX, randAppleY = randAppleGen()

def game_intro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    intro = False
                if event.key == pygame.K_q:
                    pygame.quit()

        screen.fill(WHITE)
        message("Welcome to slither", GREEN, -100, 'large')
        message("This game is fucking old shit",BLACK,-30)
        message("Dont play if u don't want to waste your free time",BLACK,10)
        message("Good Luck!",BLACK,50)
        message("P/s: Press P to play or Q to quit and C to pause in game",BLACK,180)
        pygame.display.update()
        clock.tick(FPS)
    

def snake(snakelist,BLOCK_SIZE):
    # make snake's head turn by press arrow key
    if direction == "right":
        head = pygame.transform.rotate(headofsnake, 270)
    if direction == "left":
        head = pygame.transform.rotate(headofsnake, 90)
    if direction == "up":
        head = headofsnake
    if direction == "down":
        head = pygame.transform.rotate(headofsnake, 180)
    # draw snake's head
    screen.blit(head, (snakelist[-1][0], snakelist[-1][1]))
    # draw snake's part
    for XnY in snakelist[:-1]:
        pygame.draw.rect(screen, GREEN, [XnY[0],XnY[1],BLOCK_SIZE,BLOCK_SIZE])

def text_objects(text,color,size):
    if size == 'med2':
        textSurface = medfont_4_gameover.render(text, True, color)
    if size == 'small':  
        textSurface = smallfont.render(text, True, color)
    if size == 'medium':  
        textSurface = medfont.render(text, True, color)
    if size == 'large':  
        textSurface = largefont.render(text, True, color)


    return textSurface, textSurface.get_rect()

def message(msg, color, y_display = 0,size = 'small'):
    textSurf, textRect = text_objects(msg,color,size)
#   screen_text = font.render(msg, True, color)
#   screen.blit(screen_text, [WIDTH / 2, HEIGHT / 2])
    textRect.center = (WIDTH/2), (HEIGHT/2) + y_display
    screen.blit(textSurf, textRect)
    
def gameLoop():
    
    global direction
    score1 = 0

    direction = 'right'
        
    gameOver = False
    gameExit = False
    
    lead_x = WIDTH/2
    lead_y = HEIGHT/2

    lead_x_change = BLOCK_SIZE
    lead_y_change = 0

    snakelist = []
    snakeLeight = 3

    randAppleX, randAppleY = randAppleGen()
    
    while not gameExit:
        while gameOver:
            screen.fill(BLACK)
            message("Game over",RED,-50,size = "large")
            
            message("Press R to PLAY AGAIN or Press Q to QUIT",WHITE,50,size = "med2")
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True
                    gameOver = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameOver = False    
                        gameExit = True
                        
                    if event.key == pygame.K_r:
                        gameLoop()
                    

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    gameExit = True
                    
                if event.key == pygame.K_LEFT and direction != 'right':
                    lead_x_change = -BLOCK_SIZE
                    lead_y_change = 0
                    direction = 'left'
                elif event.key == pygame.K_RIGHT and direction != 'left':
                    lead_x_change = BLOCK_SIZE
                    lead_y_change = 0
                    direction = 'right'
                elif event.key == pygame.K_UP and direction != 'down':
                    lead_x_change = 0
                    lead_y_change = -BLOCK_SIZE
                    direction = 'up'
                elif event.key == pygame.K_DOWN and direction != 'up':
                    lead_x_change = 0
                    lead_y_change = BLOCK_SIZE
                    direction = 'down'
                elif event.key == pygame.K_c:
                    pause()
        if lead_x + BLOCK_SIZE >= WIDTH or lead_x < 0 or lead_y + BLOCK_SIZE >= HEIGHT or lead_y < 0:
            gameOver = True

            
        lead_x += lead_x_change
        lead_y += lead_y_change
        screen.fill(WHITE)

        screen.blit(appleimg, (randAppleX, randAppleY))
        
        
        snakeHead = [] # X and Y of snake
        snakeHead.append(lead_x)
        snakeHead.append(lead_y)
        snakelist.append(snakeHead)

        if len(snakelist) > snakeLeight and len(snakelist) != 3:
            del snakelist[0]

        for eachSegment in snakelist[:-1]:
            if eachSegment == snakeHead:
                gameOver = True

        
        snake(snakelist,BLOCK_SIZE)

        score(score1)
        
        pygame.display.update()

        #Collision
        if lead_x >= randAppleX and lead_x <= randAppleX + APPLE_SIZE or lead_x + BLOCK_SIZE >= randAppleX and lead_x + BLOCK_SIZE <= randAppleX + APPLE_SIZE:
            if lead_y >= randAppleY and lead_y <= randAppleY + APPLE_SIZE:
                pygame.mixer.Sound.play(Yummi)
                randAppleX, randAppleY = randAppleGen()
                snakeLeight += 1
                score1 += 5
                
            elif lead_y + BLOCK_SIZE >= randAppleY and lead_y + BLOCK_SIZE <= randAppleY + APPLE_SIZE:
                pygame.mixer.Sound.play(Yummi)
                randAppleX, randAppleY = randAppleGen()
                snakeLeight += 1
                score1 += 5
                

        clock.tick(FPS)

    pygame.quit()


game_intro()
gameLoop()


