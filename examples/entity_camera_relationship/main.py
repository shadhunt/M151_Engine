

import pygame
import sys
from pathlib import Path

FRAMEWORK_ROOT = str( Path(__file__).resolve().parents[2])
DEBUG = False
if DEBUG:
    print(f"FRAMEWORK_ROOT: {FRAMEWORK_ROOT}")

sys.path.append(FRAMEWORK_ROOT)

#set project path
from properties import FONT_SIZE, SCALE, PADDING, LABEL_H, WINDOW_SIZE, FPS , TRANSPARENT_COLOR, STEP_PIXEL_PER_SEC
from config.analog_control_const import UP, UP_LEFT, UP_RIGHT, RIGHT, LEFT, DOWN_LEFT, DOWN, DOWN_RIGHT
from gameengine.actions.unit_actions.main_character_actions import load_character_frames, get_direction, show_character_test_screen
import gameengine.actions.map_actions.map_actions as map_actions
from utils.keyboard_controller import KeyboardController


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Test")
    screen = pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE)
    frames = load_character_frames()
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, FONT_SIZE)
    texture_surface = font.render("Hello, Craig", True,(255,255,255))



    keyboard_controller = KeyboardController (STEP_PIXEL_PER_SEC)


    print("Jackal is starting")

    starting_x = 0
    starting_y = 0

    #position and movement
    x=starting_x
    y=starting_y
    #starting direction
    current_direction=UP


    running = True

    layout = [
        [UP_LEFT, UP, UP_RIGHT, RIGHT],
        [LEFT, DOWN_LEFT, DOWN, DOWN_RIGHT],
    ]

    #pygame.display.flip() #show it


    while running:

        #show_character_test_screen(screen, layout, frames, font, padding, scale, label_h)
        
        dt = clock.tick(FPS)/1000.0   # CAP AT 60FPS, dt = seconds since last frame
        # make game dialog closeabled
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            #if event.type == pygame.VIDEORESIZE:   #handled automatically in pygame 2.x
            #   screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)

            #key input
        

        #this line below must be outside the event for loop, otherwise, holding the key will have 1 sec delay before it continues moving
        #by putting outside the for loop and in the game main loop, it will be run as check key press every frame actively
        #if putting inside the for event loop, that will rely on the keyboard event, that's rely on the operating system
        current_direction,x,y = keyboard_controller.actionPerform(x,y,current_direction,dt)   
        
        scaled= get_direction(SCALE,frames,current_direction)
        #display text
        screen.fill(TRANSPARENT_COLOR)  #erase everything , must be put within main loop and before drawing
        #screen.blit(texture_surface, (x,y))  #draw stuff
        screen.blit(scaled, (x, y))
        pygame.display.flip() #show it

    pygame.quit()
    sys.exit()





