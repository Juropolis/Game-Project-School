#imports
import os 
import pygame
import time
import random
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


#start game
running = True

while running == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    #initiate screen
    screen.fill((0, 0, 0,))
    pygame.draw.rect(screen, colour, pygame.Rect(15, 15, 60, 60))
    pygame.display.flip()
    