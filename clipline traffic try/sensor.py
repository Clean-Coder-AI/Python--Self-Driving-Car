import pygame
import math
import utils

class Sensor:
    def __init__(self, player_car):
        self.car = player_car
        self.ray_count = 5
        self.ray_length = 150
        self.ray_spread = math.pi / 2
        self.rays = []
        self.readings = []

    def update(self, road_borders,traffics):
        self.cast_rays()
        self.readings = []
        for ray in self.rays:
            self.readings.append(self.get_reading(ray, road_borders, traffics))

 
    def get_reading(self, ray, road_borders, traffics):
        touches = []

        for border in road_borders:
            touch = utils.get_intersection(ray[0], ray[1], border[0], border[1])
            if touch:
                touches.append(touch)

        # for traffic in traffics:
        #     for line in ray_lines:
        #         intersection_points = traffic.rect.clipline(line)
        #         if intersection_points:
        #             for point in intersection_points:
        #                 touches.append({'x': point[0], 'y': point[1], 'offset': 0})
        
        for traffic in traffics:
            poly = traffic.polygon
            for i in range(len(poly)):
                p1 = poly[i]
                p2 = poly[(i + 1) % len(poly)]
                touch = utils.get_intersection(ray[0], ray[1], p1, p2)
                if touch:
                    touches.append(touch)
            
        if not touches:
            return None
        
        else:
            offsets = [touch['offset'] for touch in touches]
            min_offset = min(offsets)
            return next(touch for touch in touches if touch['offset'] == min_offset)

    def cast_rays(self):
        self.rays = []
        # self.ray_lines=[]
        for i in range(self.ray_count):
            ray_angle = self.car.angle + utils.lerp(
                self.ray_spread / 2,
                -self.ray_spread / 2,
                0.5 if self.ray_count == 1 else i / (self.ray_count - 1)
            )

            start = {'x': self.car.x, 'y': self.car.y}
            end = {
                'x': self.car.x - math.sin(ray_angle) * self.ray_length,
                'y': self.car.y - math.cos(ray_angle) * self.ray_length
            }
            # # Extract coordinates and create (x1, y1, x2, y2) tuple
            # ray = (
            #     start['x'], start['y'],  # x1, y1
            #     end['x'], end['y']      # x2, y2
            # )
            # self.ray_lines.append(ray)
            self.rays.append([start, end])

    def draw(self, screen, camera_y):
        for i in range(self.ray_count):
            end = self.rays[i][1]
            if self.readings[i]:
                end = self.readings[i]

            pygame.draw.line(screen, (0, 255, 0), (self.rays[i][0]['x'], self.rays[i][0]['y'] - camera_y), (end['x'], end['y'] - camera_y), 2)

            if self.readings[i]:
                pygame.draw.line(screen, (255, 0, 0), (self.rays[i][1]['x'], self.rays[i][1]['y'] - camera_y), (end['x'], end['y'] - camera_y), 2)
