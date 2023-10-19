import pygame

class Road:
    def __init__(self, width, height, lane_count=3, window_width=800, window_height=600):
        self.width=width
        self.height=height  
        self.lane_count=lane_count
        self.window_width=window_width
        self.window_height=window_height

        #Calculate the road position 
        self.x=(window_width-width)/2
        self.y=(height-window_height)/2 

        #Calculate road borders which we will use for sensor and collision detection
        top_left={'x':self.x, 'y':self.y}
        top_right={'x':self.x+self.width, 'y':self.y}
        bottom_left={'x':self.x, 'y':self.y+self.height}
        bottom_right={'x':self.x+self.width, 'y':self.y+self.height}

        self.borders=[
            [top_left, bottom_left],
            [top_right, bottom_right]
        ]    

    def get_lane_center(self, lane_index):
        lane_width=self.width/self.lane_count
        return self.x +lane_width*lane_index +lane_width/2

    def draw(self, screen, camera_y):
        road_color=(128,128,128) #gray
        lane_color=(255,255,255) #white
        border_color=(255,255,0) #yellow
        border_width=5

        lane_width=self.width/self.lane_count

        #Fill the road area with the road color
        pygame.draw.rect(screen, road_color, (self.x, self.y-camera_y, self.width, self.height))

        #Draw road borders 
        pygame.draw.line(screen, border_color, (self.x, self.y-camera_y),(self.x, self.y-camera_y+self.height), border_width)
        pygame.draw.line(screen, border_color, (self.x+self.width, self.y-camera_y),(self.x+self.width, self.y-camera_y+self.height), border_width)

        #Draw dashed lines for inner lanes
        dash_length=20
        lane_thickness=5
        for i in range(1,self.lane_count):
            x=self.x+ lane_width*i
            for y in range(0,self.height,dash_length*2):
                pygame.draw.line(screen, lane_color, (x,y+self.y-camera_y), (x, y+dash_length+self.y-camera_y), lane_thickness)