import pygame 

#initialise class
class EnemyHitbox(object):
    def __init__(self, x, y):
        self.rect = pygame.Rect(x,y,70,70)
        

