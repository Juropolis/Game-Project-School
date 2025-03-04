import pygame

class Coin(object):
    def __init__(self, x, y):
        self.rect = pygame.Rect(x,y,20,20)
        