#########################################
# Programmer: Ariel Chouminov
# Date: 04/12/2016
# File Name: tetris_template3.py
# Description: This program is the third game template for our Tetris game.
#########################################
from tetris_classes import *
from random import randint
import pygame
pygame.init()

#For mac, ensures files are referenced in current working directory
import os
import sys
os.chdir(sys.path[0])

#Set title for the window
pygame.display.set_caption('Tetris')

#Fonts
font = pygame.font.SysFont("Arial Black",13)

HEIGHT = 600
WIDTH  = 800
GRIDSIZE = HEIGHT//24
screen=pygame.display.set_mode((WIDTH,HEIGHT))
GREY = (192,192,192)
WHITE = (255,255,255)

COLUMNS = 10
ROWS = 22
LEFT = 11
RIGHT = LEFT + COLUMNS
MIDDLE = LEFT + COLUMNS//2
TOP = 1
FLOOR = 22

#Makes the blocks move alittle slower
slowTime = 0
gameSpeed = 1

#Game variables
score = 0
lines = 0
level = 1
lines = 0
tetris = False

#Images
background = pygame.image.load("Images/background.png")
background = pygame.transform.scale(background, (WIDTH,HEIGHT))
introBackground = pygame.image.load("Images/intro-background.png")
introBackground = pygame.transform.scale(introBackground, (WIDTH,HEIGHT))
gameOverBackground = pygame.image.load("Images/game-over-background.png")
gameOverBackground = pygame.transform.scale(gameOverBackground, (WIDTH,HEIGHT))
pauseScreenBackground = pygame.image.load("Images/pause-screen-background.png")
pauseScreenBackground = pygame.transform.scale(pauseScreenBackground, (WIDTH,HEIGHT))

shapeImageWidth = 80
shapeImageHeight = 50

#Shape Images
shapeArrow = pygame.image.load("Images/shape-arrow.png").convert_alpha()
shapeArrow = pygame.transform.scale(shapeArrow, (shapeImageWidth, shapeImageHeight))

shapeBackL = pygame.image.load("Images/shape-backl.png").convert_alpha()
shapeBackL = pygame.transform.scale(shapeBackL, (shapeImageWidth, shapeImageHeight))

shapeBackZ = pygame.image.load("Images/shape-backz.png").convert_alpha()
shapeBackZ = pygame.transform.scale(shapeBackZ, (shapeImageWidth, shapeImageHeight))

shapeL = pygame.image.load("Images/shape-l.png").convert_alpha()
shapeL = pygame.transform.scale(shapeL, (shapeImageWidth, shapeImageHeight))

shapeLine = pygame.image.load("Images/shape-line.png").convert_alpha()
shapeLine = pygame.transform.scale(shapeLine, (shapeImageWidth, shapeImageHeight))

shapeSquare = pygame.image.load("Images/shape-square.png").convert_alpha()
shapeSquare = pygame.transform.scale(shapeSquare, (shapeImageWidth, shapeImageHeight))

shapeZ = pygame.image.load("Images/shape-z.png").convert_alpha()
shapeZ = pygame.transform.scale(shapeZ, (shapeImageWidth, shapeImageHeight))

shapeEmpty = pygame.image.load("Images/shape-empty.png").convert_alpha()
shapeEmpty = pygame.transform.scale(shapeEmpty, (shapeImageWidth, shapeImageHeight))

#Objects
shapeNo = randint(1,7)
shape = Shape(COLUMNS / 2 + COLUMNS, 1, shapeNo)
floor = Floor(LEFT,FLOOR,COLUMNS)
leftWall = Wall(LEFT-1, TOP, ROWS)
rightWall = Wall(RIGHT, TOP, ROWS)
obstacles = Obstacles(LEFT, FLOOR)
ghostShape = Shadow(COLUMNS / 2 + COLUMNS, 1, shapeNo)
gameOverBlock = Shape(COLUMNS / 2 + COLUMNS, 1, 7)

#For hold and next features
holdShape = 1
hold = False
nextShapes = [randint(1,7), randint(1,7)]

#Screen Variables
introScreen = True
instructionsScreen = False
mainScreen = False
gameOverScreen = False
pauseScreen = False

def reset(score, lines, level, tetris, shape, ghostShape, obstacles) :
    score = 0
    lines = 0
    level = 1
    tetris = False
    shapeNo = randint(1,7)
    shape = Shape(COLUMNS / 2 + COLUMNS, 1, shapeNo)
    ghostShape = Shadow(COLUMNS / 2 + COLUMNS, 1, shapeNo)
    obstacles.clear()
    obstacles = Obstacles(LEFT, FLOOR)
    score = 0

def buttonClickedDetection(leftX, rightX, upY, downY):
    """
        Takes in the left, right, up and down coordinates of the buttons and then
        detects if it is pressed within the screen.
         """
    if pygame.mouse.get_pressed()[0]:
        mouse = pygame.mouse.get_pos()
        

        if rightX > mouse[0] > leftX and downY > mouse[1] > upY:
            return True

def gameoverscreen():
    global introScreen
    global gameOverScreen
    
    screen.blit(gameOverBackground, (0,0, WIDTH, HEIGHT))
    if pygame.mouse.get_pressed()[0]:
        mouse = pygame.mouse.get_pos()

        startBtnXLeft = 320
        startBtnXRight = 385
        startBtnYUp = 385
        startBtnYDown = 430
        
        if buttonClickedDetection(startBtnXLeft, startBtnXRight, startBtnYUp, startBtnYDown):
            gameOverScreen = False
            introScreen = True

    pygame.display.update()


def pausescreen():
    global introScreen
    global mainScreen
    global gameOverScreen
    global pauseScreen
    
    screen.blit(pauseScreenBackground, (0,0, WIDTH, HEIGHT))
    if pygame.mouse.get_pressed()[0]:
        mouse = pygame.mouse.get_pos()
        print(mouse)
        
        #Resume button
        resumeBtnXLeft = 320
        resumeBtnXRight = 475
        resumeBtnYUp = 220
        resumeBtnYDown = 250
        
        if buttonClickedDetection(resumeBtnXLeft, resumeBtnXRight, resumeBtnYUp, resumeBtnYDown):
            pauseScreen = False
            mainScreen = True
        
        #Quit button
        quitBtnXLeft = 320
        quitBtnXRight = 480
        quitBtnYUp = 390
        quitBtnYDown = 425
        
        if buttonClickedDetection(quitBtnXLeft, quitBtnXRight, quitBtnYUp, quitBtnYDown):
            pauseScreen = False
            introScreen = True
    pygame.display.update()

#Main Functions
def redraw_screen():
    global mainScreen
    global gameOverScreen
    global pauseScreen
    global font
    global score
    global lines
    global level
    
    #Blit the background
    screen.blit(background, (0,0, WIDTH, HEIGHT))
    
    #Blit the score, level and Lines
    screen.blit(font.render(str(score), 1, WHITE),(140,385))
    screen.blit(font.render(str(level), 1, WHITE),(140,445))
    screen.blit(font.render(str(lines), 1, WHITE),(140,505))
    
    #Draws the objects
    shape.draw(screen, GRIDSIZE)
    ghostShape.draw(screen, GRIDSIZE)
    obstacles.draw(screen, GRIDSIZE)
#    gameOverBlock.draw(screen, GRIDSIZE)
    listOfShapeImages = [shapeBackZ,shapeZ,shapeL, shapeBackL, shapeLine, shapeArrow, shapeSquare]

    #Code for next and hold features
    if hold == True:
        shapeToDraw = listOfShapeImages[holdShape - 1]
        screen.blit(shapeToDraw, (105,110,150,150))

    shapeToNext1 = nextShapes[-2]
    shapeToNext2 = nextShapes[-1]
    shapeToNextDraw1 = shapeZ
    shapeToNextDraw2 = shapeZ

    shapeToNextDraw1 = listOfShapeImages[shapeToNext1 -1]
    shapeToNextDraw2 = listOfShapeImages[shapeToNext2 -1]

    screen.blit(shapeToNextDraw1, (620,135,150,150))
    screen.blit(shapeToNextDraw2, (620,230,150,150))

#Pause button
    pauseBtnXLeft = 720
    pauseBtnXRight = 780
    pauseBtnYUp = 520
    pauseBtnYDown = 580

    if buttonClickedDetection(pauseBtnXLeft, pauseBtnXRight, pauseBtnYUp, pauseBtnYDown):
        mainScreen = False
        pauseScreen = True
                
    #Update the display
    pygame.display.update()



def introscreen():
    global introScreen
    global mainScreen
    screen.blit(introBackground, (0,0, WIDTH, HEIGHT))

    #Button Clicked detection
    if pygame.mouse.get_pressed()[0]:
        mouse = pygame.mouse.get_pos()
        
        startBtnXLeft = 310
        startBtnXRight = 490
        startBtnYUp = 222
        startBtnYDown = 260
        
        if startBtnXRight > mouse[0] > startBtnXLeft and  startBtnYDown > mouse[1] > startBtnYUp:
            introScreen = False
            mainScreen = True

inPlay = True
while inPlay:
    #Turn off game if exited from window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            inPlay = False

    #Enters the intro screen
    if introScreen:
        introscreen()
        pygame.display.update()

    if instructionsScreen:
        instructions()
        pygame.display.update()

    #Enters the game screen
    if mainScreen:
    #Changes game speed based on the level which is based on the score.
        if score > 500 and score < 1000:
            level = 2
            gameSpeed = 5

        elif score > 1000:
            level = 3
            gameSpeed = 10
        
        keys = pygame.key.get_pressed() #the list that contains the keys pressed

        if keys[pygame.K_UP]:
            if shape.collides(obstacles) == False and shape.collides(floor) == False and shape.collides(rightWall) == False and shape.collides(leftWall) == False:
                shape.rotateClkwise()
                ghostShape.update(shape)
            
            if shape.collides(obstacles) or shape.collides(floor) or shape.collides(rightWall) or shape.collides(leftWall):
                shape.rotateCntclkwise()
                ghostShape.update(shape)

        if keys[pygame.K_LEFT]:
            if shape.collides(leftWall) == False and shape.collides(obstacles) == False:
                shape.move_left()
                ghostShape.update(shape)

            if shape.collides(leftWall) == True or shape.collides(obstacles) == True:
                shape.move_right()
                ghostShape.update(shape)

        if keys[pygame.K_RIGHT]:
            if shape.collides(rightWall) == False and shape.collides(obstacles) == False:
                shape.move_right()
                ghostShape.update(shape)
            
            if shape.collides(rightWall) == True or shape.collides(obstacles) == True:
                shape.move_left()
                ghostShape.update(shape)

        if keys[pygame.K_DOWN]:
            #If it hits another shape
            shape.move_down()
            if shape.collides(obstacles) or shape.collides(floor):
                shape.move_up()
                obstacles.append(shape)
                fullRows = obstacles.findFullRows(TOP, FLOOR, COLUMNS)
                obstacles.removeFullRows(fullRows)
                #Adds score based on lines cleared
                if 0 < len(fullRows) < 4:
                    score += 100 * len(fullRows)
                    tetris = False
                elif len(fullRows) >= 4 and tetris == False:
                    score += 800
                    tetris = True
                elif len(fullRows) >= 4 and tetris == True:
                    score += 800
                lines += len(fullRows)
                shapeNo = nextShapes[-2]
                nextShapes.append(randint(1,7))
                shape = Shape(COLUMNS / 2 + COLUMNS, 1, shapeNo)
                ghostShape = Shadow(COLUMNS / 2 + COLUMNS, 1, shapeNo)
                ghostShape.update(shape)

        if keys[pygame.K_SPACE]:
            while shape.collides(floor) == False and shape.collides(obstacles) == False:
                    shape.move_down()
        
#if it hits floor or obstacles
            if shape.collides(obstacles) or shape.collides(floor):
                shape.move_up()
                obstacles.append(shape)
                fullRows = obstacles.findFullRows(TOP, FLOOR, COLUMNS)
                obstacles.removeFullRows(fullRows)
                #Adds score based on lines cleared
                if 0 < len(fullRows) < 4:
                    score += 100 * len(fullRows)
                    tetris = False
                elif len(fullRows) >= 4 and tetris == False:
                    score += 800
                    tetris = True
                elif len(fullRows) >= 4 and tetris == True:
                    score += 800
                lines += len(fullRows)
                shapeNo = nextShapes[-2]
                nextShapes.append(randint(1,7))
                shape = Shape(COLUMNS / 2 + COLUMNS, 1, shapeNo)
                ghostShape = Shadow(COLUMNS / 2 + COLUMNS, 1, shapeNo)
                ghostShape.update(shape)

        if keys[pygame.K_c]:
            #Check if the row of the current shape isn't too low
            if shape.row < 10:
                #If they click hold and there is already item there
                if hold == True:
                    shape = Shape(COLUMNS / 2 + COLUMNS, 1, holdShape)
                    temp = shapeNo
                    shapeNo = holdShape
                    holdShape = temp
                #Otherwise, no item is there, means its the beginning of the game
                else:
                    shapeNo = nextShapes[-2]
                    nextShapes.append(randint(1,7))
                    shape = Shape(COLUMNS / 2 + COLUMNS, 1,  shapeNo)
                    hold = True

        pygame.time.delay(50)
        slowTime += gameSpeed

        if slowTime % 10 == 0:
            shape.move_down()
            if shape.collides(obstacles) or shape.collides(floor):
                if shape.collides(gameOverBlock):
                    #Game over
                    reset(score, lines, level, tetris, shape, ghostShape, obstacles)
                    mainScreen = False
                    gameOverScreen = True
                
                shape.move_up()
                obstacles.append(shape)
                fullRows = obstacles.findFullRows(TOP, FLOOR, COLUMNS)
                obstacles.removeFullRows(fullRows)
                #Adds score based on lines cleared
                if 0 < len(fullRows) < 4:
                    score += 100 * len(fullRows)
                    tetris = False
                elif len(fullRows) >= 4 and tetris == False:
                    score += 800
                    tetris = True
                elif len(fullRows) >= 4 and tetris == True:
                    score += 800
                lines += len(fullRows)
            
                shapeNo = nextShapes[-2]
                nextShapes.append(randint(1,7))
                shape = Shape(COLUMNS / 2 + COLUMNS, 1, shapeNo)
                ghostShape = Shadow(COLUMNS / 2 + COLUMNS, 1, shapeNo)
                ghostShape.clr = 2

        ghostShape.moveToBottom(floor, obstacles)
        redraw_screen()

    if pauseScreen:
        pausescreen()
        pygame.display.update()

    if gameOverScreen:
        gameoverscreen()
            
    pygame.time.delay(30)
    
pygame.quit()
    
    
