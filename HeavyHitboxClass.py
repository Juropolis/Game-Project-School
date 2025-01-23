import pygame

#initialise heavyhitbox class
class HeavyHitbox(object):
    def __init__(self, x, y):
        self.rect = pygame.Rect(x,y,70,70)