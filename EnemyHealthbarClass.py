import pygame

class EnemyHealthbar(object):
    def __init__(self, x, y, healthMultiplier, owner):
        self.rect = pygame.Rect(x,y,40*healthMultiplier,10)
        self.owner = owner
        healthMultiplier
        