#imports
import sys
import os 
import pygame
import time
import random
from PlayerClass import Player
from WallClass import Wall
from LevelFile import levels
from WaterClass import Water
from EnemyClass import Enemy

#variable initialising
playerColour = (204, 255, 109)
enemyColour = (254, 69, 69)
wallColour = (155, 155, 155)
waterColour = (200, 250, 241)
currentScore = 0
gameState = "menus"
currentLevel = 0
#holds the current amount of levels in the list
maxLevel = len(levels) - 1

#This is used for the dash ability
playerFacing = "right"
dashCooldown = 0
dashCooldownTime = 1400

#draws the screen excluding the player 
def drawBlankScreen(a, b, c):
    screen.fill((a, b, c))
    pygame.draw.rect(screen, playerColour, pygame.Rect(0,0,0,0))
    pygame.display.flip() 

#draws the screen including the player
def drawScreen(a, b, c, walls, waters):
    screen.fill((a, b, c,))
    pygame.draw.rect(screen, playerColour, player.rect)
    for wall in walls:
        pygame.draw.rect(screen,wallColour,wall.rect) 
    for water in waters:
        pygame.draw.rect(screen,waterColour,water.rect)
    for Enemy in enemies:
        pygame.draw.rect(screen, enemyColour, Enemy.rect)

    pygame.draw.rect(screen,(255,0,0),end_rect)
    pygame.display.flip()


#start pygame
os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()

#set up display
pygame.display.set_caption("Upgraded")
width = 1050
height = 600
screen = pygame.display.set_mode((width, height))

#initiate classes
clock = pygame.time.Clock()
player = Player() 
enemies = []
walls = []
waters = []
player.rect.left = 30
player.rect.top = 285


#draws first level [Without this first level wont appear until after delay]
x = y = 0
for row in levels[currentLevel]:
    for col in row:
        if col == "W":
            walls.append(Wall(x, y))
        if col == "E":
            end_rect = pygame.Rect(x,y,30,60)
        if col == "B":
            waters.append(Water(x, y))
        if col == "N":
            enemies.append(Enemy(x, y))
        x += 30
    y += 30
    x = 0

#start game
running = True

#Game loop
while running == True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        if gameState == "endScreen":
            userInput = pygame.key.get_pressed()
            if userInput[pygame.K_RETURN]:
                running = False
                pygame.quit()
                sys.exit()


    
    #sets to current game time
    currentTime = pygame.time.get_ticks()
    
    #loop for menus
    if gameState == "menus":
        drawBlankScreen(255, 255, 255)
        while gameState == "menus":
           userInput = pygame.key.get_pressed()
           if userInput[pygame.K_RETURN]:
                gameState = "playing"
           drawBlankScreen(255, 255, 255)
           for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
           

    #loop for gameplay
    if gameState == "playing":

         #player movement
        userInput = pygame.key.get_pressed()
        if userInput[pygame.K_a]:
            playerFacing = "left"
            if player.rect.x >= 3:
                player.move(-3, 0, walls, waters)
            else: 
                player.rect.x = 0
    
        if userInput[pygame.K_d]:
            playerFacing = "right"
            if player.rect.x <= width - 33:
                player.move(3, 0, walls, waters)
            else:
                player.rect.x = width - 30

        if userInput[pygame.K_w]:
            playerFacing = "up"
            if player.rect.y >= 3:
                player.move(0, -3, walls, waters)
            else:
                player.rect.y = 0
    
        if userInput[pygame.K_s]:
            playerFacing = "down"
            if player.rect.y <= height - 33:
                player.move(0, 3, walls, waters)
            else:
                player.rect.y = height - 30

        #dash ability
        if userInput[pygame.K_SPACE] and currentTime > dashCooldown:
            
            if playerFacing == "left":
                #Loop stops player position being reset multiple times
                dashLoop = True
                for i in range(1,20):
                    if player.rect.x >= 10:
                        player.move(-10, 0, walls, waters)
                        drawScreen(0, 0, 0, walls, waters)
                        time.sleep(0.01)
                    elif dashLoop == True:
                        player.rect.x = 0
                        dashLoop = False
                        drawScreen(0, 0, 0, walls, waters)
                        time.sleep(0.01)
            
            if playerFacing == "right":
                #Loop stops player position being reset multiple times
                dashLoop = True
                for i in range(1,20):
                    if player.rect.x <= width - 40:
                        player.move(10, 0, walls, waters)
                        drawScreen(0, 0, 0, walls, waters)
                        time.sleep(0.01)
                    elif dashLoop == True:
                        player.rect.x = width - 30
                        dashLoop = False
                        drawScreen(0, 0, 0, walls, waters)
                        time.sleep(0.01)
            
            if playerFacing == "up":
                #Loop stops player position being reset multiple times
                dashLoop = True
                for i in range(1,20):
                    if player.rect.y >= 10:
                        player.move(0, -10, walls, waters)
                        drawScreen(0, 0, 0, walls, waters)
                        time.sleep(0.01)
                    elif dashLoop == True:
                        player.rect.y = 0
                        dashLoop = False
                        drawScreen(0, 0, 0, walls, waters)
                        time.sleep(0.01)
            
            if playerFacing == "down":
                #Loop stops player position being reset multiple times
                dashLoop = True
                for i in range(1,20):
                    if player.rect.y <= height - 40:
                        player.move(0, 10, walls, waters)
                        drawScreen(0, 0, 0, walls, waters)
                        time.sleep(0.01)
                    elif dashLoop == True:
                        player.rect.y = height - 30
                        dashLoop = False
                        drawScreen(0, 0, 0, walls, waters)
                        time.sleep(0.01)

            #sets cooldown time
            dashCooldown = currentTime + dashCooldownTime
        
        #detects if player touches the exit door
        if player.rect.colliderect(end_rect):
            #stops code trying to load a non existent level
            if currentLevel < maxLevel:
                currentLevel = currentLevel + 1
                del walls[:]
                del waters[:]
                del enemies[:]
                x = y = 0
                for row in levels[currentLevel]:
                    for col in row:
                        if col == "W":
                            walls.append(Wall(x, y))
                        if col == "E":
                            end_rect = pygame.Rect(x,y,30,60)
                        if col == "B":
                            waters.append(Water(x, y))
                        if col == "N":
                            enemies.append(Enemy())

                        x += 30
                    y += 30 
                    x = 0
            elif currentLevel == maxLevel:
                gameState = "endScreen"
            player.rect.left = 30
            player.rect.top = 285

        for Enemy in enemies:
            if player.rect.x > Enemy.rect.x:
                Enemy.move(2, 0, walls, waters, enemies)
            if player.rect.x < Enemy.rect.x:
                Enemy.move(-2, 0, walls, waters, enemies)
            if player.rect.y < Enemy.rect.y:
                Enemy.move(0, -2, walls, waters, enemies)
            if player.rect.y > Enemy.rect.y:
                Enemy.move(0, 2, walls, waters, enemies)

        
                   
    #draw screen
    if gameState == "endScreen":
        drawBlankScreen(0, 0, 0)
    else:
        drawScreen(0, 0, 0, walls, waters)







 




    



