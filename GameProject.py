#imports
import os 
import pygame
import time
import random
from PlayerClass import Player
from WallClass import Wall


colour = (254, 36, 82)

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
wall_colour = (255, 255, 255)
current_score = 0

#start game
running = True

#Game loop
while running == True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    #player movement
    user_input = pygame.key.get_pressed()
    if user_input[pygame.K_a]:
        if player.rect.x >= 3:
            player.move(-3, 0, walls)
        else: 
            player.rect.x = 0
    
    if user_input[pygame.K_d]:
        if player.rect.x <= width - 33:
            player.move(3, 0, walls)
        else:
            player.rect.x = width - 30

    if user_input[pygame.K_w]:
        if player.rect.y >= 3:
            player.move(0, -3, walls)
        else:
            player.rect.y = 0
    
    if user_input[pygame.K_s]:
        if player.rect.y <= height - 33:
            player.move(0, 3, walls)
        else:
            player.rect.y = height - 30

    
    
            


    #draw screen
    screen.fill((0, 0, 0,))
    pygame.draw.rect(screen, colour, player.rect)
    pygame.display.flip()





 




    



