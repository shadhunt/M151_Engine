import pygame
import json
from pathlib import Path

class Main:
    def __init__(self):
        pygame.init()
        SCREEN_WIDTH=960
        SCREEN_HEIGHT=640
        screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
        self.clock  = pygame.time.Clock()
        
        map_path = Path("asssets/maps/test_map.tmj")
        map_dir = map_path.parent

        with open(map_path, "r", encoding="utf-8") as file:
            map_data = json.load(file)

        tile_width = map_data["tilewidth"]
        tile_height = map_data["tileheight"]

        tileset_data= map_data["tileset"][0]

    def game_loop(self):

if __name__ == "__main__":
    main=Main()
    main.game_loop()