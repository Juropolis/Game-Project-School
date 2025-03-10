import pygame

#initialise wall class
class Pillar(object):
    def __init__(self, wx, wy):
        self.rect = pygame.Rect(wx, wy, 30, 30)