import pygame
import sys
from pathlib import Path


FRAMEWORK_ROOT = str(Path(__file__).resolve().parents[1])
sys.path.append(FRAMEWORK_ROOT)
from config.properties import *
from config.path_config import *

from gameplay.spawner.enemy_spawner import EnemySpawner
from gameplay.graphics.graphic_loader import GraphicLoader

#enemy_json_path = Path(FRAMEWORK_ROOT) / "config" / "enemy_config.json"
enemy_json_path =  "config/practice_level/enemies.json"



class Main:
    def __init__(self):
        # Your core program logic goes here
        print("Hello from the Enemy Spawner Test!")
        print("root path:", FRAMEWORK_ROOT)
        # initialize pygame and create a window, also required by graphic_loader
        pygame.init()
        pygame.display.set_caption("Enemy Spawner Example")
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))

        graphic_loader = GraphicLoader(CHAR_SHEET)
        self.map_surface       = pygame.image.load(str(MAP_IMAGE)).convert()
        self.map_w, self.map_h = self.map_surface.get_size()
        self.enemies = []
        spawner = EnemySpawner(enemy_json_path, graphic_loader, self.map_w, self.map_h)
        self.enemies = spawner.load_enemy()
        
        for enemy in self.enemies:
            print(f"Enemy ID: {enemy.id}, Position: ({enemy.world_x}, {enemy.world_y})")
if __name__ == "__main__":
    main = Main()
    #main.game_loop()