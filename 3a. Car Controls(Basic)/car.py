import pygame

import controls

class PlayerCar:
    def __init__(self, x, y,width,height):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.player_image=pygame.image.load('car.png').convert_alpha()

        self.controls=controls.Controls()

    
    def update(self, keys):
        self.controls.update(keys)
        
        if self.controls.forward:
            self.y-=3
        if self.controls.reverse:
            self.y+=3
        if self.controls.left:
            self.x-=3
        if self.controls.right:
            self.x+=3


    def draw(self, screen):
        small_car_surface=pygame.transform.scale(self.player_image, (self.width, self.height))
        screen.blit(small_car_surface, (self.x, self.y))
