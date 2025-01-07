import pygame

#initialise enemy class
class Enemy(object):
    def __init__(self, x, y):
        self.rect = pygame.Rect(x,y,30,30)
        
    def move(self, dx, dy, walls, waters):
        if dx != 0:
            self.move_single_axis(dx, 0, walls, waters)
        if dy != 0:
            self.move_single_axis(0, dy, walls, waters)
    def move_single_axis(self, dx, dy, walls, waters):
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
        for water in waters:
            if self.rect.colliderect(water.rect):
                if dx > 0:
                    self.rect.right = water.rect.left
                if dx < 0:
                    self.rect.left = water.rect.right
                if dy > 0:
                    self.rect.bottom = water.rect.top
                if dy < 0:
                    self.rect.top = water.rect.bottom