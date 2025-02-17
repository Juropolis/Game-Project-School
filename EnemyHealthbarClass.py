import pygame

class EnemyHealthbar(object):
    def __init__(self, x, y, owner):
        self.rect = pygame.Rect(x,y,80,10)
        self.owner = owner
        