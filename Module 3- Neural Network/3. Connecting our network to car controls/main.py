import pygame

import car
import road 

pygame.init()

window_width=800
window_height=600

screen=pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Self Driving Car")
icon=pygame.image.load("logo.png").convert_alpha()
pygame.display.set_icon(icon)

#Create our road object
road_width=200
road_height=10000 #infinitely long
our_road=road.Road(road_width, road_height, lane_count=3)

#Create the PlayerCar object at the center of the screen
player_car=car.Car(our_road.get_lane_center(1), 10000, 30, 45, "PLAYER")

#Array of Traffic Objects
traffics=[
    car.Car(our_road.get_lane_center(1), 9800, 30, 45, "TRAFFIC", max_speed=2)
]


#Camera offset to follow the car on the y-axis
camera_y_offset = 500

#Game loop
clock=pygame.time.Clock()
running=True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
    
    #Check for keyboard inputs
    keys=pygame.key.get_pressed()

    #Calculate camera's y-value based on car's position
    camera_y=player_car.y-camera_y_offset

    #Clear the screen (fill with a background color)
    screen.fill((255, 255, 255))  # White background
    
    #Draw our road
    our_road.draw(screen, camera_y)

    #Update the player car
    player_car.update(keys, our_road.borders, traffics)
    #Draw the player car
    player_car.draw(screen, camera_y)

    for traffic in traffics:
        traffic.update(None,[],[])
        traffic.draw(screen, camera_y)

    #Update the display
    pygame.display.flip()

pygame.quit()