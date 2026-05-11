
'''
import pygame
import sys
from pathlib import Path

FRAMEWORK_ROOT = str( Path(__file__).resolve().parents[1])    # set parents level to 2 if want to run in template folder directly, otherwise, set to 1
DEBUG = True
if DEBUG:
    print(f"FRAMEWORK_ROOT: {FRAMEWORK_ROOT}")
sys.path.append(FRAMEWORK_ROOT)

from gameplay.actions.unit_actions.main_character_actions import load_character_frames, get_direction, show_character_test_screen
from utils.keyboard_controller import KeyboardController

class Main:
    def __init__(self):
        #initialization
        pygame.init()
        pygame.display.set_caption("Test")
        self.screen = pygame.display.set_mode((640,480), pygame.RESIZABLE)
        step=200
        self.keyboard_controller = KeyboardController(step)    
        self.frame = load_character_frames()
        self.running = True

    def game_loop(self):
        #game loop
        while(self.running):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

#main method
if __name__== "__main__":
    main=Main()
    main.game_loop()
'''