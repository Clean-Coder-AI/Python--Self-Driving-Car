import pygame
import math

import utils

class Sensor:
    def __init__(self,car):
        self.car=car
        self.ray_count=5
        self.ray_length=150
        self.ray_spread=math.pi/2

        self.rays=[]
        self.readings=[]
    
    def update(self, road_borders, traffics):
        self.cast_rays()
        self.readings=[]
        for i in range(len(self.rays)):
            self.readings.append(
                self.get_readings(self.rays[i], road_borders, traffics)
            )

    def get_readings(self, ray, road_borders, traffics):
        touches=[]
        for border in road_borders:
            touch=utils.get_intersection(
                ray[0],
                ray[1],
                border[0],
                border[1]
            )
            if touch:
                touches.append(touch)
        
        for traffic in traffics:
            poly=traffic.polygon
            for i in range(len(poly)):
                value=utils.get_intersection(
                    ray[0],
                    ray[1],
                    poly[i],
                    poly[(i+1)%len(poly)]
                )
                if value:
                    touches.append(value)
        if not touches:
            return None
        else:
            offsets=[touch['offset'] for touch in touches]
            min_offset=min(offsets)
            return next(touch for touch in touches if touch['offset'] == min_offset)
            
    
    def cast_rays(self):
        self.rays=[]
        for i in range(self.ray_count):
            ray_angle=utils.lerp(
                self.ray_spread/2,
                -self.ray_spread/2,
                0.5 if self.ray_count==1 else i/(self.ray_count-1)
            )+self.car.angle

            start={'x':self.car.x,
                   'y':self.car.y
            }       
            end={
                'x':self.car.x- math.sin(ray_angle)*self.ray_length,
                'y':self.car.y- math.cos(ray_angle)*self.ray_length
            }
            self.rays.append([start,end])

    def draw(self, screen, camera_y):
        line_width=2
        sensor_color=(0,255,0) #green
        detection_color=(255,0,0) #red

        for i in range(self.ray_count):
            end=self.rays[i][1]
            if self.readings[i]:
                end=self.readings[i]
            pygame.draw.line(screen, sensor_color, (self.rays[i][0]['x'], self.rays[i][0]['y']-camera_y), (end['x'], end['y']-camera_y), line_width)
            if self.readings[i]: 
                pygame.draw.line(screen, detection_color, (end['x'], end['y']-camera_y), (self.rays[i][1]['x'], self.rays[i][1]['y']-camera_y), line_width)

        
