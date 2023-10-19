import pygame

class Controls:
    def __init__(self):
        self.forward=False
        self.left=False
        self.right=False
        self.reverse=False
    
    def update(self, keys):
        self.forward=keys[pygame.K_UP]
        self.left=keys[pygame.K_LEFT]
        self.right=keys[pygame.K_RIGHT]
        self.reverse=keys[pygame.K_DOWN]


 
