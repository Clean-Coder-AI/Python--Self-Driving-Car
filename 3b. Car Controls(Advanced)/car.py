import pygame
import math

import controls

class PlayerCar:
    def __init__(self, x, y,width,height):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.player_image=pygame.image.load('car.png').convert_alpha()

        self.controls=controls.Controls()

        #Advanced controls attributes
        self.speed=0
        self.acceleration=0.2
        self.max_speed=3
        self.friction=0.05
        self.angle=0


    
    def update(self, keys):
        self.controls.update(keys)
        self.move()
        
    def move(self):
        if self.controls.forward:
            self.speed+=self.acceleration
        if self.controls.reverse:
            self.speed-=self.acceleration

        if self.speed>self.max_speed:
            self.speed=self.max_speed
        if self.speed<-self.max_speed/2:
            self.speed=-self.max_speed/2

        if self.speed>0:
            self.speed-=self.friction
        if self.speed<0:
            self.speed+=self.friction
        if abs(self.speed)<self.friction:
            self.speed=0

        if self.speed!=0:
            flip=1 if self.speed>0 else -1
            if self.controls.left:
                self.angle+=0.03*flip
            if self.controls.right:
                self.angle-=0.03*flip

        self.x-=math.sin(self.angle)*self.speed
        self.y-=math.cos(self.angle)*self.speed

    def draw(self, screen):
        small_car_surface=pygame.transform.scale(self.player_image, (self.width, self.height))
        rotated_image=pygame.transform.rotate(small_car_surface, math.degrees(self.angle))
        new_rect=rotated_image.get_rect(center=(self.x,self.y))
        screen.blit(rotated_image, new_rect.topleft)
