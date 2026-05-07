import pygame
import sys
from pathlib import Path

FRAMEWORK_ROOT = str( Path(__file__).resolve().parents[2])    # set parents level to 2 if want to run in template folder directly, otherwise, set to 1
DEBUG = True
if DEBUG:
    print(f"FRAMEWORK_ROOT: {FRAMEWORK_ROOT}")
sys.path.append(FRAMEWORK_ROOT)

from gameengine.actions.unit_actions.main_character_actions import load_character_frames, get_direction, show_character_test_screen
from utils.keyboard_controller import KeyboardController

def init():
    #initialization
    pygame.init()
    pygame.display.set_caption("Test")
    screen = pygame.display.set_mode((640,480), pygame.RESIZABLE)
    step=200
    keyboard_controller = KeyboardController(step)    
    frame = load_character_frames()
    return True


def game_loop(running: bool):
    #game loop
    while(running):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

#main method
if __name__== "__main__":
    running=init()
    game_loop(running)

