import pygame
import car
import controls
import road

pygame.init()

window_width = 800
window_height = 600

screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Self Driving Car")
icon = pygame.image.load("logo.png").convert_alpha()
pygame.display.set_icon(icon)

# Create the Road object
road_width = 200 
road_height=10000
road = road.Road(road_width, road_height, lane_count=3, window_width=window_width, window_height=window_height)


def generate_cars(N, road):
    player_cars = []
    for _ in range(N):
        car_instance = car.Car(road.get_lane_center(1), 10000, 30, 45, "PLAYER")
        player_cars.append(car_instance)
    return player_cars

N = 10
player_cars = generate_cars(N, road)

#array of traffic cars
traffics = [
    car.Car(road.get_lane_center(1), 9800, 30, 45,"TRAFFIC",2),
    # car.Car(road.get_lane_center(0), 9600, 30, 45,"TRAFFIC",2),
    # car.Car(road.get_lane_center(2), 9600, 30, 45,"TRAFFIC",2),
    # car.Car(road.get_lane_center(1), 9400, 30, 45,"TRAFFIC",2),
    # car.Car(road.get_lane_center(0), 9400, 30, 45,"TRAFFIC",2),
    # car.Car(road.get_lane_center(1), 9200, 30, 45,"TRAFFIC",2),
    # car.Car(road.get_lane_center(2), 9200, 30, 45,"TRAFFIC",2)
]
#controls intance
controlsP=controls.Controls("PLAYER")
controlsT=controls.Controls("TRAFFIC")

# Camera offset to follow the car on the y-axis
camera_y_offset = 450

#store the initial positions of cars, and best brain 
initial_player_positions = [(car.x, car.y) for car in player_cars]
initial_traffic_positions = [(car.x, car.y) for car in traffics]
best_brain=None

def restart_game():
    if best_brain:
        best_car.brain = best_brain
        

    for i, player_car in enumerate(player_cars):
        player_car.x, player_car.y = initial_player_positions[i]
        player_car.damaged = False        

    for i, traffic_car in enumerate(traffics):
        traffic_car.x, traffic_car.y = initial_traffic_positions[i]
    
    # if best_brain:
    #     player_cars[0].brain = best_brain

#button properties
restart_button = pygame.Rect(10, 10, 100, 50)
save_button = pygame.Rect(640, 10, 150, 50)
button_font = pygame.font.Font(None, 36)
button_colors = {
    "idle": (0, 0, 0),
    "hover": (128, 128, 128),
    "click": (0, 255, 0),
}
restart_button_state="idle"
save_button_state="idle"

# Game loop
running = True
clock = pygame.time.Clock()
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEMOTION:
            # Check if the mouse is hovering over the buttons
            if restart_button.collidepoint(event.pos):
                restart_button_state = "hover"
            else:
                restart_button_state = "idle"

            if save_button.collidepoint(event.pos):
                save_button_state = "hover"
            else:
                save_button_state = "idle"
                
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if restart_button.collidepoint(event.pos):
                restart_button_state="click"
                restart_game()
                
            elif save_button.collidepoint(event.pos):
                save_button_state="click"
                best_brain = best_car.brain

        # Update controls based on keyboard events
        controlsP.update(event)
        controlsT.update(event)

    #best car with least y-value
    best_car = min(player_cars, key=lambda c: c.y)

    # Calculate the camera's y-coordinate based on the car's position
    camera_y = best_car.y - camera_y_offset

    screen.fill((255, 255, 255)) #white

    # Draw the road with camera_y offset
    road.draw(screen, camera_y)

    #update and draw player car
    for p in player_cars: 
        p.update(controlsP, road.get_borders(), traffics)
        if p == best_car:
            p.draw(screen, camera_y, draw_sensor=True)
        else:
            p.draw(screen, camera_y)

    #update and draw the traffic cars
    for traffic_car in traffics:
        traffic_car.update(controlsT, road.get_borders(),[])
        traffic_car.draw(screen, camera_y)

    #restart button
    restart_button_color = button_colors[restart_button_state]
    pygame.draw.rect(screen, restart_button_color, restart_button)
    restart_text = button_font.render("Restart", True, (255, 255, 255))
    screen.blit(restart_text, (20, 20))

    #save brain button 
    save_button_color = button_colors[save_button_state]
    pygame.draw.rect(screen, save_button_color, save_button)
    save_text = button_font.render("Save Brain", True, (255, 255, 255))
    screen.blit(save_text, (650, 20))

    # Update the display
    pygame.display.update()

pygame.quit()