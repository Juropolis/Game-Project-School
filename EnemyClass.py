import pygame


#initialise enemy class
class Enemy(object):
    def __init__(self, x, y):
        self.rect = pygame.Rect(x,y,30,30)
        self.health = 80
        #if > 0 the enemy is immune to damage
        self.damageTimer = 0
        #Allows attack cancelling to still work with the damageTimer
        self.previousAttackRecieved = ""
        #Allows knockback to work
        self.beingAttacked = False 
    
    def recieveDamage(self, damage):
        self.health = self.health - damage
        if self.health < 0:
            self.health = 0
        
        
    def move(self, dx, dy, walls, waters, enemies, player):
        if dx != 0:
            self.move_single_axis(dx, 0, walls, waters, enemies, player)
        if dy != 0:
            self.move_single_axis(0, dy, walls, waters, enemies, player)
    def move_single_axis(self, dx, dy, walls, waters, enemies, player):
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
        for Enemy in enemies:
            if Enemy is not self and self.rect.colliderect(Enemy.rect):
                if dx > 0:
                    self.rect.right = Enemy.rect.left
                if dx < 0:
                    self.rect.left = Enemy.rect.right
                if dy > 0:
                    self.rect.bottom = Enemy.rect.top
                if dy < 0:
                    self.rect.top = Enemy.rect.bottom
        if self.rect.colliderect(player.rect):
                if dx > 0:
                    self.rect.right = player.rect.left
                if dx < 0:
                    self.rect.left = player.rect.right
                if dy > 0:
                    self.rect.bottom = player.rect.top
                if dy < 0:
                    self.rect.top = player.rect.bottom
 
        
                   



        