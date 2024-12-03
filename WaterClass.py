import pygame

#initialise wall class
class Water(object):
    def __init__(self, wx, wy):
        self.rect = pygame.Rect(wx, wy, 30, 30)