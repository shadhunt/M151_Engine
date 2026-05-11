import pygame
import sys
from pathlib import Path

'''
This is a example of using the whole framework to create a simple game with a player that can move around a map.
'''

FRAMEWORK_ROOT = str( Path(__file__).resolve().parents[1])    # set parents level to 2 if want to run in template folder directly, otherwise, set to 1
DEBUG = True
if DEBUG:
    print(f"FRAMEWORK_ROOT: {FRAMEWORK_ROOT}")
sys.path.append(FRAMEWORK_ROOT)
from config.properties import *
from config.path_config import *
from core.entities.entity import Entity
from core.camera.camera import Camera
from gameplay.graphics.graphic_loader import GraphicLoader

class Main:
    def __init__(self):
        #initialization
        pygame.init()
        pygame.display.set_caption("Test")
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        step=200
        self.clock = pygame.time.Clock()

        # Load assets
        self.map_surface      = pygame.image.load(str(MAP_IMAGE)).convert()
        self.map_w, self.map_h     = self.map_surface.get_size()

        frames           = GraphicLoader.load_frames(CHAR_SHEET)
        # Spawn the player near the center of the world map
        if DEBUG:
            print("main:",self.map_w, self.map_h)
        self.player = Entity(world_x=self.map_w / 2, world_y=self.map_h / 2, frames=frames)
        self.camera = Camera(SCREEN_W, SCREEN_H, self.player)

        self.running = True

    def game_loop(self):
        #game loop
        while(self.running):
            dt = self.clock.tick(60) / 1000.0   
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

            # ── Update ──────────────────────────────────────────────────────────
            # 1. Move the entity in world space.

            self.player.update(dt, self.map_w, self.map_h)

            # 2. Update the camera AFTER the entity moves.
            #    This ensures the camera tracks the entity's NEW position.
            #    (If you swapped these, the camera would always be one frame behind.)
            self.camera.follow(self.player, self.map_w, self.map_h)

            # ── Draw ────────────────────────────────────────────────────────────
            # Drawing order matters: map first, then entities on top.

            # 3. Draw the visible slice of the world map.
            self.camera.draw_map(self.screen, self.map_surface)

            # 4. Convert the entity's world position to screen position, then draw.
            #    This single line IS the entity–camera relationship in practice:
            #        subtract camera → get screen coordinates → draw there.
            screen_x, screen_y = self.camera.world_to_screen(self.player.world_x, self.player.world_y)
            self.player.draw(self.screen, screen_x, screen_y)

            # 5. Debug overlay (drawn last so it appears on top of everything)
            #draw_debug(self.screen, self.font, self.player, self.camera)

            pygame.display.flip()
#main method
if __name__== "__main__":
    main=Main()
    main.game_loop()

