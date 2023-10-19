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

def generate_cars(N):
    player_cars = []
    for _ in range(N):
        player_cars.append(car.Car(our_road.get_lane_center(1), 10000, 30, 45, "PLAYER"))
    return player_cars

N = 20
player_cars = generate_cars(N)

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

    #best car with least y-value
    best_car = min(player_cars, key=lambda c: c.y)

    #Calculate camera's y-value based on car's position
    camera_y=best_car.y-camera_y_offset

    #Clear the screen (fill with a background color)
    screen.fill((255, 255, 255))  # White background
    
    #Draw our road
    our_road.draw(screen, camera_y)

    #Draw and Update the player cars
    for player in player_cars:
        player.update(keys, our_road.borders, traffics)
        if player==best_car:
            player.draw(screen, camera_y, draw_sensor=True)
        else:
            player.draw(screen, camera_y)

    for traffic in traffics:
        traffic.update(None,[],[])
        traffic.draw(screen, camera_y)

    #Update the display
    pygame.display.flip()

pygame.quit()