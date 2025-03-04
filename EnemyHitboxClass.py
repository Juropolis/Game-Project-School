import pygame 

#initialise class
class EnemyHitbox(object):
    def __init__(self, x, y, owner):
        self.rect = pygame.Rect(x,y,70,70)
        self.owner = owner
        self.timer = 40

        

