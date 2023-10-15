import pygame

class Controls:
    def __init__(self,control_type):
        self.forward=False
        self.left=False
        self.right=False
        self.reverse=False

        self.control_type=control_type
    
    def update(self, keys):
        if self.control_type=="TRAFFIC":
            self.forward=True
        else:
            self.forward=keys[pygame.K_UP]
            self.left=keys[pygame.K_LEFT]
            self.right=keys[pygame.K_RIGHT]
            self.reverse=keys[pygame.K_DOWN]
        


 
