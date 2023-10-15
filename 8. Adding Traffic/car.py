import pygame
import math

import controls
import sensor

class Car:
    def __init__(self, x, y,width,height, control_type, max_speed=3):
        self.x=x
        self.y=y
        self.width=width
        self.height=height

        self.player_image=pygame.image.load('car.png').convert_alpha()
        self.damaged_image=pygame.image.load('damaged_car.png').convert_alpha()
        self.traffic_image=pygame.image.load('traffic.png').convert_alpha()

        self.control_type=control_type
        self.controls=controls.Controls(control_type)

        #Advanced controls attributes
        self.speed=0
        self.acceleration=0.2
        self.max_speed=max_speed
        self.friction=0.05
        self.angle=0

        if control_type=="PLAYER":
            self.sensor=sensor.Sensor(self)

        self.damaged=False
    

        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
        self.polygon=self.polygon_points(self.rect)

    
    def update(self, keys, road_borders, border_lines, traffics):
        if not self.damaged:
            self.controls.update(keys)
            self.move()
            self.rect.topleft = (self.x, self.y)
            self.polygon=self.polygon_points(self.rect)
            self.damaged=self.check_damage(border_lines,traffics)
        if hasattr(self,'sensor'):
            self.sensor.update(road_borders, traffics)
        
    def check_damage(self, border_lines, traffics):
        for line in border_lines:
            if self.rect.clipline(line):
                print("Collide!")
                return True     
        for traffic in traffics:
            if self.rect.colliderect(traffic.rect):
                return True     
             
        return False

    def polygon_points(self, rect):
        points = [
        {'x': rect.left, 'y': rect.top},         
        {'x': rect.right, 'y': rect.top},        
        {'x': rect.left, 'y': rect.bottom},      
        {'x': rect.right, 'y': rect.bottom}      
    ]
        return points
        
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

    def draw(self, screen, camera_y):
        if self.control_type=="PLAYER":
            if self.damaged:
                image_to_draw=self.damaged_image
            else:
                image_to_draw=self.player_image

            self.sensor.draw(screen, camera_y)
        
        else:
            image_to_draw=self.traffic_image

        small_car_surface=pygame.transform.scale(image_to_draw, (self.width, self.height))
        rotated_image=pygame.transform.rotate(small_car_surface, math.degrees(self.angle))
        new_rect=rotated_image.get_rect(center=(self.x,self.y-camera_y))
        screen.blit(rotated_image, new_rect.topleft)


