import pygame

class PlayerHealthbar(object):
    def __init__(self, x, y):
        self.rect = pygame.Rect(x,y,400,50)
        