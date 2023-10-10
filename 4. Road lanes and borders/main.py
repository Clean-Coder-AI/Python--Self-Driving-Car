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
road_height=window_height
our_road=road.Road(road_width, road_height, lane_count=3)

#Create the PlayerCar object at the center of the screen
player_car=car.PlayerCar(our_road.get_lane_center(1), window_height-45, 30, 45)

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

    #Clear the screen (fill with a background color)
    screen.fill((255, 255, 255))  # White background
    
    #Draw our road
    our_road.draw(screen)

    #Update the player car
    player_car.update(keys)

    #Draw the player car
    player_car.draw(screen)

    #Update the display
    pygame.display.update()

pygame.quit()