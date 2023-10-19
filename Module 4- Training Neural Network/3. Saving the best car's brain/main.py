import pygame
import pickle

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
    player_cars=[]
    for _ in range(N):
        player_cars.append(car.Car(our_road.get_lane_center(1), 10000, 30, 45, "PLAYER"))
    return player_cars

N=20
player_cars=generate_cars(N)
try:
    with open('brain.txt','rb') as b:
        player_cars[0].brain=pickle.load(b)
except FileNotFoundError:
    print('no file')
except Exception as e:
    print('error', e)

def save_brain():
    best_brain = best_car.brain
    with open('brain.txt','wb') as f:
        for _ in range(N):
            pickle.dump(best_brain,f)

#Array of Traffic Objects
traffics=[
    car.Car(our_road.get_lane_center(1), 9800, 30, 45, "TRAFFIC", max_speed=2)
]

#Camera offset to follow the car on the y-axis
camera_y_offset=500

#button properties
save_button=pygame.Rect(640, 10, 150, 50)
button_font= pygame.font.Font(None, 36)
button_colors={
    "idle": (0, 0, 0),
    "hover": (128, 128, 128),
    "click": (0, 255, 0),
}
save_button_state="idle"

#Game loop
clock=pygame.time.Clock()
running=True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        elif event.type==pygame.MOUSEMOTION:
            if save_button.collidepoint(event.pos):
                save_button_state="hover"
            else:
                save_button_state="idle"
                
        elif event.type==pygame.MOUSEBUTTONDOWN:               
            if save_button.collidepoint(event.pos):
                save_button_state="click"
                save_brain()
    
    #Check for keyboard inputs
    keys=pygame.key.get_pressed()

    #best car with least y-value
    best_car=min(player_cars, key=lambda c: c.y)

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
    
    #save brain button 
    save_button_color=button_colors[save_button_state]
    pygame.draw.rect(screen, save_button_color, save_button)
    save_text=button_font.render("Save Brain", True, (255, 255, 255))
    screen.blit(save_text, (650,20))

    #Update the display
    pygame.display.flip()

pygame.quit()