#imports
import os 
import pygame
import time
import random
from PlayerClass import Player
from WallClass import Wall

#variable initialising
colour = (254, 36, 82)

playerFacing = "right"

dashCooldown = 0
dashCooldownTime = 1400




#start pygame
os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()

#set up display
pygame.display.set_caption("Upgraded")
width = 768
height = 435
screen = pygame.display.set_mode((width, height))

#initiate classes
clock = pygame.time.Clock()
player = Player() 
walls = []
wallColour = (255, 255, 255)
currentScore = 0
gameState = "menus"

#start game
running = True

#Game loop
while running == True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    currentTime = pygame.time.get_ticks()
    
    if gameState == "menus":
        print("hehe menus")
        gameState = "playing"

    if gameState == "playing":

         #player movement
        userInput = pygame.key.get_pressed()
        if userInput[pygame.K_a]:
            playerFacing = "left"
            if player.rect.x >= 3:
                player.move(-3, 0, walls)
            else: 
                player.rect.x = 0
    
        if userInput[pygame.K_d]:
            playerFacing = "right"
            if player.rect.x <= width - 33:
                player.move(3, 0, walls)
            else:
                player.rect.x = width - 30

        if userInput[pygame.K_w]:
            playerFacing = "up"
            if player.rect.y >= 3:
                player.move(0, -3, walls)
            else:
                player.rect.y = 0
    
        if userInput[pygame.K_s]:
            playerFacing = "down"
            if player.rect.y <= height - 33:
                player.move(0, 3, walls)
            else:
                player.rect.y = height - 30

        if userInput[pygame.K_SPACE] and currentTime > dashCooldown:
            if playerFacing == "left":
                dashLoop = True
                for i in range(1,20):
                    if player.rect.x >= 10:
                        player.move(-10, 0, walls)
                        screen.fill((0, 0, 0,))
                        pygame.draw.rect(screen, colour, player.rect)
                        pygame.display.flip()
                        time.sleep(0.01)
                    elif dashLoop == True:
                        player.rect.x = 0
                        dashLoop = False
                        screen.fill((0, 0, 0,))
                        pygame.draw.rect(screen, colour, player.rect)
                        pygame.display.flip()
                        time.sleep(0.01)
            if playerFacing == "right":
                dashLoop = True
                for i in range(1,20):
                    if player.rect.x <= width - 40:
                        player.move(10, 0, walls)
                        screen.fill((0, 0, 0,))
                        pygame.draw.rect(screen, colour, player.rect)
                        pygame.display.flip()
                        time.sleep(0.01)
                    elif dashLoop == True:
                        player.rect.x = width - 30
                        dashLoop = False
                        screen.fill((0, 0, 0,))
                        pygame.draw.rect(screen, colour, player.rect)
                        pygame.display.flip()
                        time.sleep(0.01)
            if playerFacing == "up":
                dashLoop = True
                for i in range(1,20):
                    if player.rect.y >= 10:
                        player.move(0, -10, walls)
                        screen.fill((0, 0, 0,))
                        pygame.draw.rect(screen, colour, player.rect)
                        pygame.display.flip()
                        time.sleep(0.01)
                    elif dashLoop == True:
                        player.rect.y = 0
                        dashLoop = False
                        screen.fill((0, 0, 0,))
                        pygame.draw.rect(screen, colour, player.rect)
                        pygame.display.flip()
                        time.sleep(0.01)
            if playerFacing == "down":
                dashLoop = True
                for i in range(1,20):
                    if player.rect.y <= height - 40:
                        player.move(0, 10, walls)
                        screen.fill((0, 0, 0,))
                        pygame.draw.rect(screen, colour, player.rect)
                        pygame.display.flip()
                        time.sleep(0.01)
                    elif dashLoop == True:
                        player.rect.y = height - 30
                        dashLoop = False
                        screen.fill((0, 0, 0,))
                        pygame.draw.rect(screen, colour, player.rect)
                        pygame.display.flip()
                        time.sleep(0.01)
                

            dashCooldown = currentTime + dashCooldownTime
        

    #draw screen
    screen.fill((0, 0, 0,))
    pygame.draw.rect(screen, colour, player.rect)
    pygame.display.flip()





 




    



