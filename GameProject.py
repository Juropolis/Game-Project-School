#imports
import sys
import os 
import pygame
import time
import random
import math
from pygame import mixer
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
from EnemyHealthbarBgroundClass import EnemyHealthbarBground
from PlayerHealthBarClass import PlayerHealthbar
from PlayerHealthbarBgroundClass import PlayerHealthbarBground
from CoinClass import Coin


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
healthColour = (100, 255, 100)
coinColour = (250, 220, 90)
currentScore = 0
gameState = "startMenu"
currentLevel = -1
menuOption = 2
menuCooldown = 0
difficultyOption = 2
volumeOption = 2


#score variables
Score = 0
roomTimer = 0

#Money/Shop variables
Money = 100
shopsVisited = 0


#initialise music player
mixer.init()
#load background music
mixer.music.load("BackgroundMusic.mp3")



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
SattackCooldownTime = 2600
SattackTimer = 0
ShitTimer = 24
Scollision = False

#This is used for the Enemy attack
EattackCooldownTime = 600
EattackStartup = 25

#This is used for equipping special abilities
toxicBought = False
galeBought = False
chargerBought = False

#special ability variables
galeMultiplier = 1

#start pygame
os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()

#text display variables MUST BE BELOW PYGAME.INIT()
font = pygame.font.Font(None, 54)
smallfont = pygame.font.Font(None, 20)

#set up display
pygame.display.set_caption("Upgraded")
width = 1050
height = 720
screen = pygame.display.set_mode((width, height))
#initiate classes
clock = pygame.time.Clock()
player = Player()
Lattack = LightHitbox(0, 0) 
Hattack = HeavyHitbox(0, 0)
Sattack = SpecialHitbox(0, 0)
playerHealthbar = PlayerHealthbar(120, 635)
playerHealthbarBground = PlayerHealthbarBground(120, 635)
enemies = []
walls = []
waters = []
enemyAttacks = []
enemyHealthbars = []
enemyHealthbarBgrounds = []
Coins = []
player.rect.left = 30
player.rect.top = 285
wasdMovement = False
numEnemiesRemaining = 0
end_rect = pygame.Rect(0,0,0,0)

#images
heartIMG = pygame.image.load('Heart.png')
heartIMG = pygame.transform.scale(heartIMG, (70, 70))
MenuStartIMG = pygame.image.load('MenuStart.png')
MenuStartIMG = pygame.transform.scale(MenuStartIMG, (1050, 720))
MenuSettingsIMG = pygame.image.load('MenuSettings.png')
MenuSettingsIMG = pygame.transform.scale(MenuSettingsIMG, (1050, 720))
MenuLeaderboardIMG = pygame.image.load('MenuLeaderboard.png')
MenuLeaderboardIMG = pygame.transform.scale(MenuLeaderboardIMG, (1050, 720))
SettingsVolumeIMG = pygame.image.load('SettingsVolume.png')
SettingsVolumeIMG = pygame.transform.scale(SettingsVolumeIMG, (720, 720))
SettingsDifficultyIMG = pygame.image.load('SettingsDifficulty.png')
SettingsDifficultyIMG = pygame.transform.scale(SettingsDifficultyIMG, (720, 720))
SettingsExitIMG = pygame.image.load('SettingsExit.png')
SettingsExitIMG = pygame.transform.scale(SettingsExitIMG, (720, 720))
EasyTextIMG = pygame.image.load('EasyText.png')
EasyTextIMG = pygame.transform.scale(EasyTextIMG, (160, 30))
MediumTextIMG = pygame.image.load('MediumText.png')
MediumTextIMG = pygame.transform.scale(MediumTextIMG, (240, 30))
MediumTextVolIMG = pygame.transform.scale(MediumTextIMG, (240, 30))
HardTextIMG = pygame.image.load('HardText.png')
HardTextIMG = pygame.transform.scale(HardTextIMG, (160, 30))
LowTextIMG = pygame.image.load('LowText.png')
LowTextIMG = pygame.transform.scale(LowTextIMG, (160, 30))
HighTextIMG = pygame.image.load('HighText.png')
HighTextIMG = pygame.transform.scale(HighTextIMG, (160, 30))
PauseVolumeIMG = pygame.image.load('PauseVolume.png')
PauseVolumeIMG = pygame.transform.scale(PauseVolumeIMG, (720, 720))
PauseControlsIMG = pygame.image.load('PauseControls.png')
PauseControlsIMG = pygame.transform.scale(PauseControlsIMG, (720, 720))
PauseResumeIMG = pygame.image.load('PauseResume.png')
PauseResumeIMG = pygame.transform.scale(PauseResumeIMG, (720, 720))
ShopToxicIMG = pygame.image.load('ShopToxic.png')
ShopToxicIMG = pygame.transform.scale(ShopToxicIMG, (1050, 720))
ShopGaleIMG = pygame.image.load('ShopGale.png')
ShopGaleIMG = pygame.transform.scale(ShopGaleIMG, (1050, 720))
ShopChargerIMG = pygame.image.load('ShopCharger.png')
ShopChargerIMG = pygame.transform.scale(ShopChargerIMG, (1050, 720))
ShopExitIMG = pygame.image.load('ShopExit.png')
ShopExitIMG = pygame.transform.scale(ShopExitIMG, (1050, 720))


#text variable initialisation
scoreText = font.render("", True, (225, 225, 225))
moneyText = font.render("", True, (200, 200, 0))
purchasedText = smallfont.render("", True, (225, 225, 225))







#draws the screen excluding the player 
def drawBlankScreen(a, b, c):
    screen.fill((a, b, c))
    pygame.draw.rect(screen, playerColour, pygame.Rect(0,0,0,0))
    pygame.display.flip() 

#draws any menu related screens
def drawMenus():
    if gameState == "startMenu":
        if menuOption == 1:
            screen.blit(MenuSettingsIMG, (0, 0))
        if menuOption == 2:
            screen.blit(MenuStartIMG, (0, 0))
        if menuOption == 3:
            screen.blit(MenuLeaderboardIMG, (0, 0)) 
    if gameState == "settings":
        screen.fill((200, 150, 200))
        if menuOption == 1:
            screen.blit(SettingsVolumeIMG, (165,0))
        if menuOption == 2:
            screen.blit(SettingsDifficultyIMG, (165,0))
        if menuOption == 3:
            screen.blit(SettingsExitIMG, (165,0))
        if volumeOption == 1:
            screen.blit(LowTextIMG, (565, 235))
        if volumeOption == 2:
            screen.blit(MediumTextIMG, (530, 238))
        if volumeOption == 3:
            screen.blit(HighTextIMG, (565, 235))
        if difficultyOption == 1:
            screen.blit(EasyTextIMG, (570, 428))
        if difficultyOption == 2:
            screen.blit(MediumTextIMG, (530, 428))
        if difficultyOption == 3:
            screen.blit(HardTextIMG, (570, 428))
    if gameState == "paused":

        if menuOption == 1:
            screen.blit(PauseVolumeIMG, (165, 0))
        if menuOption == 2:
            screen.blit(PauseControlsIMG, (165, 0))
        if menuOption == 3:
            screen.blit(PauseResumeIMG, (165, 0))
        if volumeOption == 1:
            screen.blit(LowTextIMG, (570, 275))
        if volumeOption == 2:
            MediumTextVolIMG = pygame.transform.scale(MediumTextIMG, (200, 30))
            screen.blit(MediumTextVolIMG, (555, 278))
            MediumTextVolIMG = pygame.transform.scale(MediumTextIMG, (240, 30))
        if volumeOption == 3:
            screen.blit(HighTextIMG, (570, 278))
    if gameState == "controls":
        screen.fill((200, 150, 200))
    if gameState == "shop":
        screen.fill((200, 150, 200))
        

        if menuOption == 1:
            screen.blit(ShopToxicIMG, (0, 0))
            if toxicBought == True:
                pygame.draw.rect(screen, (25, 25, 25), pygame.Rect(740, 340, 230, 310))
                screen.blit(purchasedText, (752, 485))

        if menuOption == 2:
            screen.blit(ShopGaleIMG, (0, 0))
            if galeBought == True:
                pygame.draw.rect(screen, (25, 25, 25), pygame.Rect(740, 340, 230, 310))
                screen.blit(purchasedText, (752, 485))

        if menuOption == 3:
            screen.blit(ShopChargerIMG, (0, 0))
            if chargerBought == True:
                pygame.draw.rect(screen, (25, 25, 25), pygame.Rect(740, 340, 230, 310))
                screen.blit(purchasedText, (752, 485))

        if menuOption == 4:
            screen.blit(ShopExitIMG, (0, 0))
        
        screen.blit(moneyText, (70, 280))

    if gameState == "endScreen":
            drawBlankScreen(20, 20, 20)
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
    for enemyHealthbarBground in enemyHealthbarBgrounds:
        pygame.draw.rect(screen, (0,0,0), enemyHealthbarBground.rect)
    for enemyHealthbar in enemyHealthbars:
        pygame.draw.rect(screen, healthColour, enemyHealthbar.rect)
    for coin in Coins:
        pygame.draw.rect(screen, coinColour, coin.rect)
    pygame.draw.rect(screen, (30, 30, 30), pygame.Rect(0,600,1050,120))
    pygame.draw.rect(screen, (0,0,0), playerHealthbarBground.rect)
    pygame.draw.rect(screen, healthColour, playerHealthbar.rect)
    pygame.draw.rect(screen, playerColour, player.rect)
    screen.blit(heartIMG, (30, 625))
    if numEnemiesRemaining == 0:
        pygame.draw.rect(screen,(255,0,0),end_rect)
    screen.blit(scoreText, (540, 642))
    screen.blit(moneyText, (810, 642))
    if gameState != "paused":
        pygame.display.flip()

#allows use of log base 3
def logBase3(x):
    return  math.log(x) / math.log(3)


currentTime = 0


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
    if gameState != "paused" and gameState != "controls":
        currentTime = currentTime + 15

    userInput = pygame.key.get_pressed()
    
    #loop for menus
    if gameState == "startMenu":
        if userInput[pygame.K_RETURN]:
            if menuCooldown == 0:
                menuCooldown = 15
                if menuOption == 1:
                    gameState = "settings"
                    menuOption = 1
                if menuOption == 2:
                    gameState = "playing"
                    #plays music
                    pygame.mixer.music.play(loops=-1)
                if menuOption == 3:
                    gameState = "leaderboard"
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
        
        #allows players to navigate menu 
        if menuCooldown == 0:
            if userInput[pygame.K_a]:
                menuCooldown = 15
                if menuOption == 1:
                    menuOption = 3
                else:
                    menuOption = menuOption - 1
            if userInput[pygame.K_d]:
                menuCooldown = 15
                if menuOption == 3:
                    menuOption = 1
                else:
                    menuOption = menuOption + 1

    elif gameState == "settings":
        if userInput[pygame.K_w]:
            if menuCooldown == 0:
                menuCooldown = 15
                if menuOption == 1:
                    menuOption = 3
                else:
                    menuOption = menuOption - 1
        if userInput[pygame.K_s]:
            if menuCooldown == 0:
                menuCooldown = 15
                if menuOption == 3:
                    menuOption = 1
                else:
                    menuOption = menuOption + 1


        if userInput[pygame.K_RETURN]:
            if menuCooldown == 0:
                if menuOption == 3:
                    gameState = "startMenu"
                    menuOption = 2
                    pygame.event.clear(pygame.KEYDOWN)
                menuCooldown = 15
        
        if userInput[pygame.K_a]:
            if menuCooldown == 0:
                if menuOption == 1:
                    if volumeOption == 1:
                        volumeOption = 3
                    else:
                        volumeOption = volumeOption - 1
                    menuCooldown = 15
                if menuOption == 2:
                    if difficultyOption == 1:
                        difficultyOption = 3
                    else:
                        difficultyOption = difficultyOption - 1
                    menuCooldown = 15
        if userInput[pygame.K_d]:
            if menuCooldown == 0:
                if menuOption == 1:
                    if volumeOption == 3:
                        volumeOption = 1
                    else:
                        volumeOption = volumeOption + 1
                    menuCooldown = 15
                if menuOption == 2:
                    if difficultyOption == 3:
                        difficultyOption = 1
                    else:
                        difficultyOption = difficultyOption + 1
                    menuCooldown = 15
                
                
        
        

           

    #loop for gameplay
    elif gameState == "playing":

        if userInput[pygame.K_RETURN]:
            if menuCooldown == 0:
                gameState = "paused"
                menuOption = 1
                menuCooldown = 15

        if userInput[pygame.K_a]:
            playerFacingX = "left"
        if userInput[pygame.K_d]:
            playerFacingX = "right"
        if userInput[pygame.K_w]:
            playerFacingY = "up"
        if userInput[pygame.K_s]:
            playerFacingY = "down"
        

        #player movement
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


        #manages player being attacked
        if  player.damageTimer == 0:
                player.beingAttacked = False 
        
        #decreases enemy timer
        if player.damageTimer > 0:
                player.damageTimer = player.damageTimer - 1

        #Manages enemy attacks 
        for attack in enemyAttacks:
            if attack.rect.colliderect(player.rect) and player.beingAttacked == False:
                player.beingAttacked = True
                player.damageTimer = 80
                player.recieveDamage(15)
                
       
        #detects if player touches the exit door
        if player.rect.colliderect(end_rect) or currentLevel == -1:
            if numEnemiesRemaining == 0:
                
                
                if currentLevel != -1:
                    #calculates score based on time
                    Score = Score + int((10000 - 1000*logBase3(roomTimer // 60)))
                roomTimer = 60
                Score = (Score // 100) * 100 

                #stops code trying to load a non existent level
                if currentLevel < maxLevel:
                    if currentLevel != 3 and currentLevel != 8 and currentLevel != 13: 
                        currentLevel = currentLevel + 1
                        del walls[:]
                        del waters[:]
                        del enemies[:]
                        del enemyHealthbars[:]
                        del enemyAttacks[:]
                        del Coins[:]
                        numEnemiesRemaining = 0
                        x = y = 0
                        for row in levels[currentLevel - shopsVisited]:
                            for col in row:
                                if col == "W":
                                    walls.append(Wall(x, y))
                                if col == "E":
                                    end_rect = pygame.Rect(x,y,30,60)
                                if col == "B":
                                    waters.append(Water(x, y))
                                if col == "N":
                                    enemies.append(Enemy(x, y, difficultyOption))
                                    numEnemiesRemaining = numEnemiesRemaining + 1
                                x += 30
                            y += 30 
                            x = 0
                        for enemy in enemies:
                            enemyHealthbars.append(EnemyHealthbar(0, 0, difficultyOption, enemy))
                            enemyHealthbarBgrounds.append(EnemyHealthbarBground(0, 0, difficultyOption, enemy))
                    
                    else:
                        gameState = "shop"
                        menuOption = 1
                        shopsVisited = shopsVisited + 1

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
                                        enemy.move(-1.4*HknockbackS*galeMultiplier, 0, walls, waters, enemies, player)
                                        if player.rect.y < enemy.rect.y:
                                            enemy.move(0, 1.4*HknockbackS*galeMultiplier, walls, waters, enemies, player)
                                        if player.rect.y > enemy.rect.y:
                                            enemy.move(0, -1.4*HknockbackS*galeMultiplier, walls, waters, enemies, player)
                                    else:
                                        enemy.move(-2*HknockbackS*galeMultiplier, 0, walls, waters, enemies, player)
                                if player.rect.x < enemy.rect.x:
                                    if player.rect.y != enemy.rect.y:
                                        enemy.move(1.4*HknockbackS*galeMultiplier, 0, walls, waters, enemies, player)
                                        if player.rect.y < enemy.rect.y:
                                            enemy.move(0, 1.4*HknockbackS*galeMultiplier, walls, waters, enemies, player)
                                        if player.rect.y > enemy.rect.y:
                                            enemy.move(0, -1.4*HknockbackS*galeMultiplier, walls, waters, enemies, player)
                                    else:
                                        enemy.move(2*HknockbackS*galeMultiplier, 0, walls, waters, enemies, player)
                                else:
                                    if player.rect.y < enemy.rect.y:
                                        enemy.move(0, 2*HknockbackS*galeMultiplier, walls, waters, enemies, player)
                                    if player.rect.y > enemy.rect.y:
                                        enemy.move(0, -2*HknockbackS*galeMultiplier, walls, waters, enemies, player)
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
                        if toxicBought == True:
                            enemy.poisonTimer = enemy.poisonTimer + 30
                        enemy.recieveDamage(10)
                        enemy.damageTimer = LhitTimer
                        enemy.previousAttackRecieved = "Light"
                        enemy.beingAttacked = True
                       
            if enemy.rect.colliderect(Hattack.rect):
                #allows attack cancelling as well as hitting the same attack again
                if enemy.previousAttackRecieved == "Light" or enemy.damageTimer == 0:
                    if heavyAttacking == True:
                        if toxicBought == True:
                            enemy.poisonTimer = enemy.poisonTimer + 40
                        enemy.recieveDamage(20)
                        enemy.damageTimer = HhitTimer
                        enemy.previousAttackRecieved = "Heavy"
                        enemy.beingAttacked = True
                        
            if enemy.rect.colliderect(Sattack.rect):
                #allows attack cancelling as well as hitting the same attack again
                if enemy.previousAttackRecieved == "Light" or enemy.previousAttackRecieved == "Heavy" or enemy.damageTimer == 0:
                    if specialAttacking == True:
                        if toxicBought == True:
                            enemy.poisonTimer = enemy.poisonTimer + 50
                        enemy.recieveDamage(30)
                        enemy.damageTimer = ShitTimer
                        enemy.previousAttackRecieved = "Special"
                        enemy.beingAttacked = True
                        

            if enemy.damageTimer > 0:
                enemy.damageTimer = enemy.damageTimer - 1
        
            if enemy.health == 0:
                for attack in enemyAttacks:
                    #identifies which enemy the attack belongs to
                    if attack.owner == enemy:
                        #removes the attack belonging to a specific enemy
                        enemyAttacks.remove(attack) 
                for enemyHealthbarBground in enemyHealthbarBgrounds:
                    #identifies which enemy the healthbar belongs to
                    if enemyHealthbarBground.owner == enemy:
                        enemyHealthbarBgrounds.remove(enemyHealthbarBground)  
                for enemyHealthbar in enemyHealthbars:
                    #identifies which enemy the healthbar belongs to
                    if enemyHealthbar.owner == enemy:
                        enemyHealthbars.remove(enemyHealthbar) 
                #increases score on defeating enemy
                Score = Score + 100
                Coins.append(Coin(enemy.rect.x + 5, enemy.rect.y + 5))    
                enemies.remove(enemy)
                numEnemiesRemaining = numEnemiesRemaining - 1
            else:
                for enemyHealthbar in enemyHealthbars:
                    #identifies which enemy the healthbar belongs to
                    if enemyHealthbar.owner == enemy:
                        enemyHealthbar.rect.width = enemy.health


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

            #does poison damage to enemies
            if enemy.poisonTimer > 0:
                enemy.recieveDamage(0.2)
                enemy.poisonTimer = enemy.poisonTimer - 1
                

            for attack in enemyAttacks:
                #identifies which enemy the attack belongs to
                if attack.owner == enemy:
                    attack.rect.x = enemy.rect.x - 20
                    attack.rect.y = enemy.rect.y - 20
                if attack.timer == 0:
                    enemyAttacks.remove(attack)
                attack.timer = attack.timer - 1
            
            #positions health bars
            for enemyHealthbar in enemyHealthbars:
                if enemyHealthbar.owner == enemy:
                    if difficultyOption == 1:
                        enemyHealthbar.rect.x = enemy.rect.x - 5
                        enemyHealthbar.rect.y = enemy.rect.y - 20
                    if difficultyOption == 2:
                        enemyHealthbar.rect.x = enemy.rect.x - 25
                        enemyHealthbar.rect.y = enemy.rect.y - 20
                    if difficultyOption == 3:
                        enemyHealthbar.rect.x = enemy.rect.x - 45
                        enemyHealthbar.rect.y = enemy.rect.y - 20
                    
            
            #positions health bar backgrounds
            for enemyHealthbarBground in enemyHealthbarBgrounds:
                if enemyHealthbarBground.owner == enemy:
                    if difficultyOption == 1:
                        enemyHealthbarBground.rect.x = enemy.rect.x - 5
                        enemyHealthbarBground.rect.y = enemy.rect.y - 20
                    if difficultyOption == 2:
                        enemyHealthbarBground.rect.x = enemy.rect.x - 25
                        enemyHealthbarBground.rect.y = enemy.rect.y - 20
                    if difficultyOption == 3:
                        enemyHealthbarBground.rect.x = enemy.rect.x - 45
                        enemyHealthbarBground.rect.y = enemy.rect.y - 20




                    


            
        
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

        #removes coins once the player touches them
        for coin in Coins:
            if player.rect.colliderect(coin.rect):
                Money = Money + 10
                Coins.remove(coin)
        

        playerHealthbar.rect.width = player.health/100 * 400
        roomTimer = roomTimer + 1

        #text rendering
        scoreText = font.render(f"Score: {Score}", True, (225, 225, 225))
        moneyText = font.render(f"Money: {Money}", True, (200, 150, 0))
        purchasedText = smallfont.render(f"You have already purchased this", True, (255, 255, 255))

        if galeBought == True:
            galeMultiplier = 2

    if gameState == "paused":
        

        if userInput[pygame.K_w]:
            if menuCooldown == 0:
                menuCooldown = 15
                if menuOption == 1:
                    menuOption = 3
                else:
                    menuOption = menuOption - 1

        if userInput[pygame.K_s]:
            if menuCooldown == 0:
                menuCooldown = 15
                if menuOption == 3:
                    menuOption = 1
                else:
                    menuOption = menuOption + 1
        
        if userInput[pygame.K_a]:
            if menuCooldown == 0:
                if menuOption == 1:
                    if volumeOption == 1:
                        volumeOption = 3
                    else:
                        volumeOption = volumeOption - 1
                    menuCooldown = 15

        if userInput[pygame.K_d]:
            if menuCooldown == 0:
                if menuOption == 1:
                    if volumeOption == 3:
                        volumeOption = 1
                    else:
                        volumeOption = volumeOption + 1
                    menuCooldown = 15

        if userInput[pygame.K_RETURN]:
            if menuCooldown == 0: 
                if menuOption == 2:
                    gameState = "controls"
                    menuCooldown = 15
                if menuOption == 3:
                    gameState = "playing"
                    menuCooldown = 15
    
    if gameState == "controls":
        if userInput[pygame.K_RETURN]:
            if menuCooldown == 0:
                gameState = "paused"
                menuCooldown = 15

    if gameState == "shop":

        moneyText = font.render(f"Money: {Money}", True, (200, 150, 0))

        if userInput[pygame.K_w]:
            if menuCooldown == 0:
                menuCooldown = 15
                if menuOption == 1:
                    menuOption = 4
                else:
                    menuOption = menuOption - 1
        if userInput[pygame.K_s]:
            if menuCooldown == 0:
                menuCooldown = 15
                if menuOption == 4:
                    menuOption = 1
                else:
                    menuOption = menuOption + 1

        if userInput[pygame.K_RETURN]:
            if menuCooldown == 0:
                menuCooldown = 15

                if menuOption == 1:
                    if Money >= 80 and toxicBought == False:
                        Money = Money - 80
                        toxicBought = True
                        
                if menuOption == 2:
                    if Money >= 140 and galeBought == False:
                        Money = Money - 140
                        galeBought = True                      

                if menuOption == 3:
                    if Money >= 320 and chargerBought == False:
                        Money = Money - 320
                        chargerBought = True
                        
                if menuOption == 4:
                    end_rect = pygame.Rect(0,0,30,30)
                    currentLevel = currentLevel + 1
                    player.rect.x = 0
                    player.rect.y = 0
                    drawBlankScreen(0, 0, 0)
                    gameState = "playing"
                    
    


                
            

    #checks if the player has died
    if player.health == 0:
        gameState = "endScreen"
        #stops the music for end screen
        mixer.music.stop()
    
    if volumeOption == 1:
        mixer.music.set_volume(0.10)
    if volumeOption == 2:
        mixer.music.set_volume(0.50)
    if volumeOption == 3:
        mixer.music.set_volume(1.00)


    
    
    
        
        

    playerFacingX = "Neutral"
    playerFacingY = "Neutral"    

    #stops menu inputs registering multiple times
    if menuCooldown > 0:
            menuCooldown = menuCooldown - 1

    #draw screen
    if gameState != "playing" and gameState != "paused":
        drawMenus()
    elif gameState == "paused":
        drawScreen(60, 60, 60,walls, waters)
        drawMenus()
    else:
        drawScreen(60, 60, 60, walls, waters)

    







 




    



