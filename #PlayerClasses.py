import pygame

#initialise player class
class Player(object):
    def __init__(self):
        self.rect = pygame.Rect(30,30,60,60)
        