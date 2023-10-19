import pygame
import car 

pygame.init()

window_width=800
window_height=600

screen=pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Self Driving Car")
icon=pygame.image.load("logo.png").convert_alpha()
pygame.display.set_icon(icon)

#Create the PlayerCar object at the center of the screen
player_car=car.PlayerCar(window_width/2-30, window_height-45, 30, 45)

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

    #Update the player car
    player_car.update(keys)

    #Draw the player car
    player_car.draw(screen)

    #Update the display
    pygame.display.flip()

pygame.quit()