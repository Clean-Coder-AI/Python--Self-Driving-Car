import pygame
import math

import controls
import sensor
import network

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
            #input layer of 5(sensor rays) neurons, hidden layer of 6 neurons,and output of 4(up,left,right,down)
            self.brain=network.NeuralNetwork([self.sensor.ray_count,6,4])

        self.damaged=False
        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
        self.polygon=self.polygon_points()

        self.use_brain=control_type=="PLAYER"
    
    def update(self, keys, road_borders, traffics):
        if not self.damaged:
            self.controls.update(keys)
            self.move()
            self.rect.topleft = (self.x, self.y)
            self.polygon=self.polygon_points()
            self.damaged=self.check_damage(road_borders,traffics)
        if hasattr(self,'sensor'):
            self.sensor.update(road_borders, traffics)
            #extract offsets from sensor readings and map them to 0 if null, otherwise 1 - offset
            offsets = [0 if reading is None else 1 - reading['offset'] for reading in self.sensor.readings]
            outputs = network.NeuralNetwork.feed_forward(offsets, self.brain)
            #to check outputs in terminal
            # print(outputs)

            if self.use_brain:
                self.controls.forward = outputs[0]
                self.controls.left = outputs[1]
                self.controls.right = outputs[2]
                self.controls.reverse = outputs[3]
        
    def check_damage(self, road_borders, traffics):
        road_lines = []
        for border in road_borders:
            top, bottom = border[0], border[1]
            road_lines.append((top, bottom))
        for line in road_lines:
            if self.rect.clipline((line[0]['x']+self.width, line[0]['y'], line[1]['x'], line[1]['y'])):
                return True  
            
        for traffic in traffics:
            if self.rect.colliderect(traffic.rect):
                return True     
             
        return False

    # def polygon_points(self, rect):
    #     points = [
    #     {'x': rect.left, 'y': rect.top},         
    #     {'x': rect.right, 'y': rect.top},        
    #     {'x': rect.left, 'y': rect.bottom},      
    #     {'x': rect.right, 'y': rect.bottom}      
    # ]
    #     return points
    def polygon_points(self):
        points=[]
        rad=math.hypot(self.width,self.height)/2
        alpha=math.atan2(self.width,self.height)
        points.append({
            'x': self.x-math.sin(self.angle-alpha)*rad,
            'y': self.y-math.cos(self.angle-alpha)*rad
        })
        points.append({
            'x': self.x-math.sin(self.angle+alpha)*rad,
            'y': self.y-math.cos(self.angle+alpha)*rad
        })
        points.append({
            'x': self.x-math.sin(math.pi+self.angle-alpha)*rad,
            'y': self.y-math.cos(math.pi+self.angle-alpha)*rad
        })
        points.append({
            'x': self.x-math.sin(math.pi+self.angle+alpha)*rad,
            'y': self.y-math.cos(math.pi+self.angle+alpha)*rad
        })
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

    def draw(self, screen, camera_y, draw_sensor=False):
        if self.control_type=="PLAYER":
            if self.damaged:
                image_to_draw=self.damaged_image
            else:
                image_to_draw=self.player_image
            if draw_sensor:
                self.sensor.draw(screen, camera_y)
        
        else:
            image_to_draw=self.traffic_image

        small_car_surface=pygame.transform.scale(image_to_draw, (self.width, self.height))
        rotated_image=pygame.transform.rotate(small_car_surface, math.degrees(self.angle))
        new_rect=rotated_image.get_rect(center=(self.x,self.y-camera_y))
        screen.blit(rotated_image, new_rect.topleft)


