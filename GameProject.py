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
from HeavyHitboxClass import HeavyHitbox
from SpecialHitboxClass import SpecialHitbox
from EnemyHitboxClass import EnemyHitbox
from EnemyHealthbarClass import EnemyHealthbar

#variable initialising
playerFacingX = "right"
playerFacingY = "up"
playerColour = (204, 255, 109)
LattackColour = (0, 255, 0)
HattackColour = (0, 0, 255)
SattackColour = (0, 155, 155)
EattackColour = (255, 165, 0)
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
directionSet = True

#holds the current amount of levels in the list
maxLevel = len(levels) - 1

#This is used for the dash ability
dashCooldown = 0
dashCooldownTime = 1400
dashTimer = 0
dashing = False

#This is used for the light attack
LattackCooldown = 0
LattackCooldownTime = 400
LattackTimer = 0
LhitTimer = 20

#This is used for the Heavy attack
HattackCooldown = 0
HattackCooldownTime = 1400
HattackTimer = 0
HhitTimer = 32

#This is used for the Special attack
SattackCooldown = 0
SattackCooldownTime = 2200
SattackTimer = 0
ShitTimer = 24
Scollision = False

#This is used for the Enemy attack
EattackCooldownTime = 600
EattackStartup = 25




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
Hattack = HeavyHitbox(0, 0)
Sattack = SpecialHitbox(0, 0)
enemies = []
walls = []
waters = []
enemyAttacks = []
enemyHealthbars = []
player.rect.left = 30
player.rect.top = 285
wasdMovement = False

#draws the screen excluding the player 
def drawBlankScreen(a, b, c):
    screen.fill((a, b, c))
    pygame.draw.rect(screen, playerColour, pygame.Rect(0,0,0,0))
    pygame.display.flip() 

#draws the screen including the player
def drawScreen(a, b, c, walls, waters):
    screen.fill((a, b, c,))
    if lightAttacking == True:
        pygame.draw.rect(screen, LattackColour, Lattack.rect)
    elif heavyAttacking == True:
        pygame.draw.rect(screen, HattackColour, Hattack.rect)
    elif specialAttacking == True:
        pygame.draw.rect(screen, SattackColour, Sattack.rect)
    else:
        pygame.draw.rect(screen, playerColour, player.rect)
    for wall in walls:
        pygame.draw.rect(screen,wallColour,wall.rect) 
    for water in waters:
        pygame.draw.rect(screen,waterColour,water.rect)
    for enemyAttack in enemyAttacks:
        pygame.draw.rect(screen, EattackColour, enemyAttack.rect)
    for enemy in enemies:
        pygame.draw.rect(screen, enemyColour, enemy.rect)
    pygame.draw.rect(screen, playerColour, player.rect)
    if numEnemiesRemaining == 0:
        pygame.draw.rect(screen,(255,0,0),end_rect)
    pygame.display.flip()

#draws first level [Without this first level wont appear until after delay]
numEnemiesRemaining = 0
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
            numEnemiesRemaining = numEnemiesRemaining + 1
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
            if playerFacingX == "left":
                
                wasdMovement = True
                if playerFacingY != "Neutral":
                    
                    if player.rect.x >= 3:
                        player.move(-3, 0, walls, waters, enemies)
                    else:
                        player.rect.x = 0

                    if playerFacingY == "up":
                        if player.rect.y >= 3:
                            player.move(0, -3, walls, waters, enemies)
                        else:
                            player.rect.y = 0

                    elif playerFacingY == "down":
                        if player.rect.y <= height - 33:
                            player.move(0, 3, walls, waters, enemies)
                        else:
                            player.rect.y = height - 30
                else:
                    if player.rect.x >= 4:
                        player.move(-4, 0, walls, waters, enemies)
                    else:
                        player.rect.x = 0


            if playerFacingX == "right":

                wasdMovement = True
                if playerFacingY != "Neutral":
                    
                    if player.rect.x <= width - 33:
                        player.move(3, 0, walls, waters, enemies)
                    else:
                        player.rect.x = 0

                    if playerFacingY == "up":
                        if player.rect.y >= 3:
                            player.move(0, -3, walls, waters, enemies)
                        else:
                            player.rect.y = 0

                    elif playerFacingY == "down":
                        if player.rect.y <= height - 33:
                            player.move(0, 3, walls, waters, enemies)
                        else:
                            player.rect.y = height - 30
                else:
                    if player.rect.x <= width - 34:
                        player.move(4, 0, walls, waters, enemies)
                    else:
                        player.rect.x = 0
            
            if playerFacingX == "Neutral":

                if playerFacingY == "up":
                        if player.rect.y >= 4:
                            player.move(0, -4, walls, waters, enemies)
                        else:
                            player.rect.y = 0

                elif playerFacingY == "down":
                    if player.rect.y <= height - 34:
                        player.move(0, 4, walls, waters, enemies)
                    else:
                        player.rect.y = height - 30

                
            

        #dash ability
        if userInput[pygame.K_SPACE] and currentTime > dashCooldown and dashing == False and (playerFacingX != "Neutral" or playerFacingY != "Neutral"):
            dashTimer = 1
            dashing = True

        if dashTimer > 0:  

            if playerFacingX == "left":
                
                wasdMovement = True
                if playerFacingY != "Neutral":
                    
                    if player.rect.x >= 14:
                        player.move(-14, 0, walls, waters, enemies)
                    else:
                        player.rect.x = 0

                    if playerFacingY == "up":
                        if player.rect.y >= 14:
                            player.move(0, -14, walls, waters, enemies)
                        else:
                            player.rect.y = 0

                    elif playerFacingY == "down":
                        if player.rect.y <= height - 44:
                            player.move(0, 14, walls, waters, enemies)
                        else:
                            player.rect.y = height - 30
                else:
                    if player.rect.x >= 14:
                        player.move(-14, 0, walls, waters, enemies)
                    else:
                        player.rect.x = 0


            if playerFacingX == "right":

                wasdMovement = True
                if playerFacingY != "Neutral":
                    
                    if player.rect.x <= width - 44:
                        player.move(14, 0, walls, waters, enemies)
                    else:
                        player.rect.x = 0

                    if playerFacingY == "up":
                        if player.rect.y >= 14:
                            player.move(0, -14, walls, waters, enemies)
                        else:
                            player.rect.y = 0

                    elif playerFacingY == "down":
                        if player.rect.y <= height - 44:
                            player.move(0, 14, walls, waters, enemies)
                        else:
                            player.rect.y = height - 30
                else:
                    if player.rect.x <= width - 44:
                        player.move(14, 0, walls, waters, enemies)
                    else:
                        player.rect.x = 0
            
            if playerFacingX == "Neutral":

                if playerFacingY == "up":
                        if player.rect.y >= 20:
                            player.move(0, -20, walls, waters, enemies)
                        else:
                            player.rect.y = 0

                elif playerFacingY == "down":
                    if player.rect.y <= height - 50:
                        player.move(0, 20, walls, waters, enemies)
                    else:
                        player.rect.y = height - 30
        else:
            dashing = False

        
        
        #Keybind for LightAttacking
        if userInput[pygame.K_u] and currentTime > LattackCooldown and currentTime > HattackCooldown and currentTime > SattackCooldown and lightAttacking == False and heavyAttacking == False and specialAttacking == False:
            lightAttacking = True

        #Keybind for HeavyAttcking
        if userInput[pygame.K_i] and currentTime > HattackCooldown and currentTime > SattackCooldown and heavyAttacking == False and specialAttacking == False:
            if lightAttacking == True:
                lightAttacking = False
            heavyAttacking = True
        
        #keybind for SpecialAttacking
        if userInput[pygame.K_o] and currentTime > SattackCooldown and specialAttacking == False and (playerFacingX != "Neutral" or playerFacingY != "Neutral"):
            #allows hitbox cancelling
            if lightAttacking == True:
                lightAttacking = False
            if heavyAttacking == True:
                heavyAttacking = False
            #starts the Special attack and allows Special attack to move
            specialAttacking = True
            Scollision = False
            #allows direction of attack to be set for each attack
            directionSet = True
            #stops cube from becoming massive overtime
            Sattack.rect.height = 60
            Sattack.rect.width = 60
                
                  
                    

        
        
        #detects if player touches the exit door
        if player.rect.colliderect(end_rect):
            if numEnemiesRemaining == 0:
                #stops code trying to load a non existent level
                if currentLevel < maxLevel:
                    currentLevel = currentLevel + 1
                    del walls[:]
                    del waters[:]
                    del enemies[:]
                    numEnemiesRemaining = 0
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
                                numEnemiesRemaining = numEnemiesRemaining + 1
                            x += 30
                        y += 30 
                        x = 0
                    for enemy in enemies:
                        enemyHealthbars.append(EnemyHealthbar(x, y, enemy))

                elif currentLevel == maxLevel:
                    gameState = "endScreen"
                player.rect.left = 30
                player.rect.top = 285

        #Enemy Code
        for enemy in enemies:
            
            #moves enemies
            if not enemy.rect.colliderect(player.rect):
                if enemy.beingAttacked == True: 

                    if enemy.previousAttackRecieved == "Light":
                        if player.rect.x > enemy.rect.x:
                            if player.rect.y != enemy.rect.y:
                                enemy.move(0.7, 0, walls, waters, enemies, player)
                                if player.rect.y < enemy.rect.y:
                                    enemy.move(0, -0.7, walls, waters, enemies, player)
                                if player.rect.y > enemy.rect.y:
                                    enemy.move(0, 0.7, walls, waters, enemies, player) 
                            else:
                                enemy.move(1, 0, walls, waters, enemies, player)
                        if player.rect.x < enemy.rect.x:
                            if player.rect.y != enemy.rect.y:
                                enemy.move(-0.7, 0, walls, waters, enemies, player)
                                if player.rect.y < enemy.rect.y:
                                    enemy.move(0, -0.7, walls, waters, enemies, player)
                                if player.rect.y > enemy.rect.y:
                                    enemy.move(0, 0.7, walls, waters, enemies, player) 
                            else:
                                enemy.move(-1, 0, walls, waters, enemies, player)
                        else:
                            if player.rect.y < enemy.rect.y:
                                enemy.move(0, -1, walls, waters, enemies, player)
                            if player.rect.y > enemy.rect.y:
                                enemy.move(0, 1, walls, waters, enemies, player)

                    if enemy.previousAttackRecieved == "Heavy":
                        if enemy.damageTimer > 20:
                            HknockbackS = 10
                            if HknockbackS > 0: 

                                if player.rect.x > enemy.rect.x:
                                    if player.rect.y != enemy.rect.y:
                                        enemy.move(-1.4*HknockbackS, 0, walls, waters, enemies, player)
                                        if player.rect.y < enemy.rect.y:
                                            enemy.move(0, 1.4*HknockbackS, walls, waters, enemies, player)
                                        if player.rect.y > enemy.rect.y:
                                            enemy.move(0, -1.4*HknockbackS, walls, waters, enemies, player)
                                    else:
                                        enemy.move(-2*HknockbackS, 0, walls, waters, enemies, player)
                                if player.rect.x < enemy.rect.x:
                                    if player.rect.y != enemy.rect.y:
                                        enemy.move(1.4*HknockbackS, 0, walls, waters, enemies, player)
                                        if player.rect.y < enemy.rect.y:
                                            enemy.move(0, 1.4*HknockbackS, walls, waters, enemies, player)
                                        if player.rect.y > enemy.rect.y:
                                            enemy.move(0, -1.4*HknockbackS, walls, waters, enemies, player)
                                    else:
                                        enemy.move(2*HknockbackS, 0, walls, waters, enemies, player)
                                else:
                                    if player.rect.y < enemy.rect.y:
                                        enemy.move(0, 2*HknockbackS, walls, waters, enemies, player)
                                    if player.rect.y > enemy.rect.y:
                                        enemy.move(0, -2*HknockbackS, walls, waters, enemies, player)
                                HknockbackS = HknockbackS - 3
                    if enemy.previousAttackRecieved == "Special":

                        if player.rect.x > enemy.rect.x:
                            if player.rect.y != enemy.rect.y:
                                enemy.move(0.6, 0, walls, waters, enemies, player)
                                if player.rect.y < enemy.rect.y:
                                    enemy.move(0, -0.6, walls, waters, enemies, player)
                                if player.rect.y > enemy.rect.y:
                                    enemy.move(0, 0.6, walls, waters, enemies, player) 
                            else:
                                enemy.move(0.9, 0, walls, waters, enemies, player)
                        if player.rect.x < enemy.rect.x:
                            if player.rect.y != enemy.rect.y:
                                enemy.move(-0.6, 0, walls, waters, enemies, player)
                                if player.rect.y < enemy.rect.y:
                                    enemy.move(0, -0.6, walls, waters, enemies, player)
                                if player.rect.y > enemy.rect.y:
                                    enemy.move(0, 0.6, walls, waters, enemies, player) 
                            else:
                                enemy.move(-0.9, 0, walls, waters, enemies, player)
                        else:
                            if player.rect.y < enemy.rect.y:
                                enemy.move(0, -0.9, walls, waters, enemies, player)
                            if player.rect.y > enemy.rect.y:
                                enemy.move(0, 0.9, walls, waters, enemies, player)
                    
                else:
                    if enemy.attacking == False:

                        if player.rect.x > enemy.rect.x:
                            if player.rect.y != enemy.rect.y:
                                enemy.move(2, 0, walls, waters, enemies, player)
                                if player.rect.y < enemy.rect.y:
                                    enemy.move(0, -2, walls, waters, enemies, player)
                                if player.rect.y > enemy.rect.y:
                                    enemy.move(0, 2, walls, waters, enemies, player) 
                            else:
                                enemy.move(3, 0, walls, waters, enemies, player)
                        elif player.rect.x < enemy.rect.x:
                            if player.rect.y != enemy.rect.y:
                                enemy.move(-2, 0, walls, waters, enemies, player)
                                if player.rect.y < enemy.rect.y:
                                    enemy.move(0, -2, walls, waters, enemies, player)
                                if player.rect.y > enemy.rect.y:
                                    enemy.move(0, 2, walls, waters, enemies, player) 
                            else:
                                enemy.move(-3, 0, walls, waters, enemies, player)
                        else:
                            if player.rect.y < enemy.rect.y:
                                enemy.move(0, -3, walls, waters, enemies, player)
                            if player.rect.y > enemy.rect.y:
                                enemy.move(0, 3, walls, waters, enemies, player)

            #calculates damage
            if enemy.rect.colliderect(Lattack.rect):
                if enemy.damageTimer == 0:
                    if lightAttacking == True:
                        enemy.recieveDamage(10)
                        enemy.damageTimer = LhitTimer
                        enemy.previousAttackRecieved = "Light"
                        enemy.beingAttacked = True
                        print(enemy.health)
            if enemy.rect.colliderect(Hattack.rect):
                #allows attack cancelling as well as hitting the same attack again
                if enemy.previousAttackRecieved == "Light" or enemy.damageTimer == 0:
                    if heavyAttacking == True:
                        enemy.recieveDamage(20)
                        enemy.damageTimer = HhitTimer
                        enemy.previousAttackRecieved = "Heavy"
                        enemy.beingAttacked = True
                        print(enemy.health)
            if enemy.rect.colliderect(Sattack.rect):
                #allows attack cancelling as well as hitting the same attack again
                if enemy.previousAttackRecieved == "Light" or enemy.previousAttackRecieved == "Heavy" or enemy.damageTimer == 0:
                    if specialAttacking == True:
                        enemy.recieveDamage(30)
                        enemy.damageTimer = ShitTimer
                        enemy.previousAttackRecieved = "Special"
                        enemy.beingAttacked = True
                        print(enemy.health)

            if enemy.damageTimer > 0:
                enemy.damageTimer = enemy.damageTimer - 1
        
            if enemy.health == 0:
                for attack in enemyAttacks:
                    #identifies which enemy the attack belongs to
                    if attack.owner == enemy:
                        #removes the attack belonging to a specific enemy
                        enemyAttacks.remove(attack)       
                enemies.remove(enemy)
                numEnemiesRemaining = numEnemiesRemaining - 1

            #recognises if the enemy is being hit by the players attacks
            if enemy.damageTimer == 0:
                enemy.beingAttacked = False

            #if enemy is using an attack
            if enemy.attacking == True: 
                if enemy.attackTimer > EattackStartup and enemy.drawAttackLoop == True:
                    #stops multiple attacks being added per enemy
                    enemy.drawAttackLoop = False
                    #adds attack to list to be drawn
                    enemyAttacks.append(EnemyHitbox(enemy.rect.x - 20, enemy.rect.y - 20, enemy))
            else:
                for attack in enemyAttacks:
                    #identifies which enemy the attack belongs to
                    if attack.owner == enemy:
                        #removes the attack belonging to a specific enemy
                        enemyAttacks.remove(attack)

            for attack in enemyAttacks:
                    #identifies which enemy the attack belongs to
                    if attack.owner == enemy:
                        attack.rect.x = enemy.rect.x - 20
                        attack.rect.y = enemy.rect.y - 20
                    
                   
                

                
        

           
        
        #sets attack box positions
        Lattack.rect.x = player.rect.x - 10
        Lattack.rect.y = player.rect.y - 10
        
        Hattack.rect.x = player.rect.x - 20
        Hattack.rect.y = player.rect.y - 20


        #So that position reset code doesn't interfere with movement
        if specialAttacking == False:
            Sattack.rect.x = player.rect.x - 15
            Sattack.rect.y = player.rect.y - 15

        #sets position light and heavy hitboxes as well as initial position of special hitbox
        if playerFacingX != "Neutral":
            if playerFacingX == "left":
                Lattack.rect.x = Lattack.rect.x - 20
                Hattack.rect.x = Hattack.rect.x - 20
                if specialAttacking == False:
                    Sattack.rect.x = Sattack.rect.x - 20
            elif playerFacingX == "right":
                Lattack.rect.x = Lattack.rect.x + 20
                Hattack.rect.x = Hattack.rect.x + 20
                if specialAttacking == False:
                    Sattack.rect.x = Sattack.rect.x + 20
        if playerFacingY != "Neutral":
            if playerFacingY == "up":
                Lattack.rect.y = Lattack.rect.y - 20
                Hattack.rect.y = Hattack.rect.y - 20
                if specialAttacking == False:
                    Sattack.rect.y = Sattack.rect.y - 20
            elif playerFacingY == "down":
                Lattack.rect.y = Lattack.rect.y + 20
                Hattack.rect.y = Hattack.rect.y + 20
                if specialAttacking == False:
                    Sattack.rect.y = Sattack.rect.y + 20

        #if the attack is being used
        if specialAttacking == True:
            #sets initial direction of movement
            if directionSet == True:
                specialTravelX = playerFacingX
                specialTravelY = playerFacingY
                #stops direction being changed after attack initially used
                directionSet = False
            #collision detections
            for enemy in enemies:
                if Sattack.rect.colliderect(enemy):
                    Scollision = True
            for wall in walls:
                if Sattack.rect.colliderect(wall):
                    Scollision = True
            for water in waters:
                if Sattack.rect.colliderect(water):
                    Scollision = True
            #if it hasn't hit anything:
            if Scollision == False:
                #movement code
                if specialTravelX == "left":
                    if specialTravelY == "up":
                        Sattack.rect.y = Sattack.rect.y - 18
                        Sattack.rect.x = Sattack.rect.x - 18
                    elif specialTravelY == "down":
                        Sattack.rect.y = Sattack.rect.y + 18
                        Sattack.rect.x = Sattack.rect.x - 18
                    else:
                        Sattack.rect.x = Sattack.rect.x - 25

                elif specialTravelX == "right":
                    if specialTravelY == "up":
                        Sattack.rect.y = Sattack.rect.y - 18
                        Sattack.rect.x = Sattack.rect.x + 18
                    elif specialTravelY == "down":
                        Sattack.rect.y = Sattack.rect.y + 18
                        Sattack.rect.x = Sattack.rect.x + 18
                    else:
                        Sattack.rect.x = Sattack.rect.x + 25
                else:
                    if specialTravelY == "up":
                        Sattack.rect.y = Sattack.rect.y - 25
                    if specialTravelY == "down":
                        Sattack.rect.y = Sattack.rect.y + 25
            else:
                #grows the special attack hitbox
                Sattack.rect.height = Sattack.rect.height + 2
                Sattack.rect.width = Sattack.rect.width + 2
                #keeps the position centered whilst growing
                Sattack.rect.x = Sattack.rect.x - 1
                Sattack.rect.y = Sattack.rect.y -1
            
            
    
                
                    
            
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
    
    #sets heavy attack cooldown 
        if HattackTimer > 16:
            heavyAttacking = False
            HattackTimer = 0
            HattackCooldown = currentTime + HattackCooldownTime
        elif heavyAttacking == True:
            HattackTimer = HattackTimer + 1

    #sets special attack cooldown 
        if Scollision == True:
            if SattackTimer > 12:
                specialAttacking = False
                SattackTimer = 0
                SattackCooldown = currentTime + SattackCooldownTime
            elif specialAttacking == True:
                SattackTimer = SattackTimer + 1
    
    #sets enemy attack cooldown
        for enemy in enemies:
            if enemy.attackTimer > EattackStartup:
                if enemy.attackTimer > EattackStartup + 40:
                    enemy.attacking = False
                    enemy.attackTimer = 0
                    enemy.attackCooldown = currentTime + EattackCooldownTime
                    enemy.drawAttackLoop = True
                    #enemyAttacks.remove()
                elif enemy.attacking == True:
                    enemy.attackTimer = enemy.attackTimer + 1
            elif enemy.attacking == True:
                enemy.attackTimer = enemy.attackTimer + 1

    
    
    
        
        

    playerFacingX = "Neutral"
    playerFacingY = "Neutral"              
    #draw screen
    if gameState == "endScreen":
        drawBlankScreen(0, 0, 0)
    elif gameState == "menus":
        drawBlankScreen(255, 255, 255)
    else:
        drawScreen(0, 0, 0, walls, waters)

    







 




    



