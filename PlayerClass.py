import pygame

#initialise player class
class Player(object):
    def __init__(self):
        self.rect = pygame.Rect(30,30,30,30)
        
    def move(self, dx, dy, walls):
        if dx != 0:
            self.move_single_axis(dx, 0, walls)
        if dy != 0:
            self.move_single_axis(0, dy, walls)
    def move_single_axis(self, dx, dy, walls):
        self.rect.x += dx
        self.rect.y += dy

        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dx > 0:
                    self.rect.right = wall.rect.left
                if dx < 0:
                    self.rect.left = wall.rect.right
                if dy > 0:
                    self.rect.bottom = wall.rect.top
                if dy < 0:
                    self.rect.top = wall.rect.bottom
                
        