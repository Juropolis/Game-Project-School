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
from LightHitboxClass import LightHitbox
#variable initialising
playerFacingX = "right"
playerFacingY = "up"
playerColour = (204, 255, 109)
LattackColour = (0, 255, 0)
enemyColour = (254, 69, 69)
wallColour = (155, 155, 155)
waterColour = (200, 250, 241)
currentScore = 0
gameState = "menus"
currentLevel = 0

#Attacking Variables
lightAttacking = False
heavyAttacking = False
specialAttacking = False

#holds the current amount of levels in the list
maxLevel = len(levels) - 1

#This is used for the dash ability
dashCooldown = 0
dashCooldownTime = 1400
dashTimer = 0
dashing = False

#This is used for the light attack
LattackCooldown = 0
LattackCooldownTime = 600
LattackTimer = 0



#draws the screen excluding the player 
def drawBlankScreen(a, b, c):
    screen.fill((a, b, c))
    pygame.draw.rect(screen, playerColour, pygame.Rect(0,0,0,0))
    pygame.display.flip() 

#draws the screen including the player
def drawScreen(a, b, c, walls, waters):
    screen.fill((a, b, c,))
    pygame.draw.rect(screen, playerColour, player.rect)
    if lightAttacking == True:
        pygame.draw.rect(screen, LattackColour, Lattack.rect)
    elif heavyAttacking == True:
        print("heavy")
    elif specialAttacking == True:
        print("special")
    else:
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
Lattack = LightHitbox(0, 0) 
enemies = []
walls = []
waters = []
player.rect.left = 30
player.rect.top = 285
wasdMovement = False

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
    wasdMovement = False
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
        if gameState == "menus":
           userInput = pygame.key.get_pressed()
           if userInput[pygame.K_RETURN]:
                gameState = "playing"
           for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
           

    #loop for gameplay
    if gameState == "playing":

        if userInput[pygame.K_a]:
            playerFacingX = "left"
        if userInput[pygame.K_d]:
            playerFacingX = "right"
        if userInput[pygame.K_w]:
            playerFacingY = "up"
        if userInput[pygame.K_s]:
            playerFacingY = "down"
        

         #player movement
        userInput = pygame.key.get_pressed()
        if dashing == False:
            if userInput[pygame.K_a]:
                wasdMovement = True
                if player.rect.x >= 3:
                    player.move(-3, 0, walls, waters, enemies)
                else: 
                    player.rect.x = 0
    
            if userInput[pygame.K_d]:
                wasdMovement = True
                if player.rect.x <= width - 33:
                    player.move(3, 0, walls, waters, enemies)
                else:
                    player.rect.x = width - 30

            if userInput[pygame.K_w]:
                wasdMovement = True
                if player.rect.y >= 3:
                    player.move(0, -3, walls, waters, enemies)
                else:
                    player.rect.y = 0
        
            if userInput[pygame.K_s]:
                wasdMovement = True
                if player.rect.y <= height - 33:
                    player.move(0, 3, walls, waters, enemies)
                else:
                    player.rect.y = height - 30

        #dash ability
        if userInput[pygame.K_SPACE] and currentTime > dashCooldown and dashing == False and (playerFacingX != "Neutral" or playerFacingY != "Neutral"):
            dashTimer = 1
            dashing = True

        if dashTimer > 0:    
            if playerFacingX == "left":
                #Loop stops player position being reset multiple times
                dashLoop = True
                if player.rect.x >= 20:
                    player.move(-20, 0, walls, waters, enemies)                       
                elif dashLoop == True:
                    player.rect.x = 0
                    dashLoop = False
                        
                
            if playerFacingX == "right":
                #Loop stops player position being reset multiple times
                dashLoop = True
                if player.rect.x <= width - 50:
                    player.move(20, 0, walls, waters, enemies)
                elif dashLoop == True:
                    player.rect.x = width - 40
                    dashLoop = False
                    
                
            if playerFacingY == "up":
                #Loop stops player position being reset multiple times
                dashLoop = True
                if player.rect.y >= 20:
                    player.move(0, -20, walls, waters, enemies)
                elif dashLoop == True:
                    player.rect.y = 0
                    dashLoop = False
                    
                    
                
            if playerFacingY == "down":
                #Loop stops player position being reset multiple times
                dashLoop = True
                if player.rect.y <= height - 50:
                    player.move(0, 20, walls, waters, enemies)               
                elif dashLoop == True:
                    player.rect.y = height - 40
                    dashLoop = False
        else:
            dashing = False
        
        #Keybind for LightAttacking
        if userInput[pygame.K_u] and currentTime > LattackCooldown and lightAttacking == False:
            lightAttacking = True
                
                  
                    

        
        
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
                            enemies.append(Enemy(x, y))

                        x += 30
                    y += 30 
                    x = 0
            elif currentLevel == maxLevel:
                gameState = "endScreen"
            player.rect.left = 30
            player.rect.top = 285

        #moves enemies
        for Enemy in enemies:
            if not Enemy.rect.colliderect(player.rect):
                if player.rect.x > Enemy.rect.x:
                    Enemy.move(2, 0, walls, waters, enemies, player)
                if player.rect.x < Enemy.rect.x:
                    Enemy.move(-2, 0, walls, waters, enemies, player)
                if player.rect.y < Enemy.rect.y:
                    Enemy.move(0, -2, walls, waters, enemies, player)
                if player.rect.y > Enemy.rect.y:
                    Enemy.move(0, 2, walls, waters, enemies, player)
        
        #sets attack box positions
        Lattack.rect.x = player.rect.x - 10
        Lattack.rect.y = player.rect.y - 10

        if playerFacingX != "Neutral":
            if playerFacingX == "left":
                Lattack.rect.x = Lattack.rect.x - 20
            elif playerFacingX == "right":
                Lattack.rect.x = Lattack.rect.x + 20
        if playerFacingY != "Neutral":
            if playerFacingY == "up":
                Lattack.rect.y = Lattack.rect.y - 20
            elif playerFacingY == "down":
                Lattack.rect.y = Lattack.rect.y + 20
                    
            
    #sets dash cooldown 
        if dashTimer > 15:
            dashTimer = 0
            dashCooldown = currentTime + dashCooldownTime
        elif dashing == True:
            dashTimer = dashTimer + 1
    
    #sets light attack cooldown 
        if LattackTimer > 10:
            lightAttacking = False
            LattackTimer = 0
            LattackCooldown = currentTime + LattackCooldownTime
        elif lightAttacking == True:
            LattackTimer = LattackTimer + 1

    playerFacingX = "Neutral"
    playerFacingY = "Neutral"              
    #draw screen
    if gameState == "endScreen":
        drawBlankScreen(0, 0, 0)
    elif gameState == "menus":
        drawBlankScreen(255, 255, 255)
    else:
        drawScreen(0, 0, 0, walls, waters)

    







 




    



