import pygame
import sys
import json
from pathlib import Path
from config.analog_control_const import *
from core.entities.enemy import Enemy
SKIN_REGISTRY = {
    "gray_vehicle": ENEMY_DIRECTION_COORDS,
}

class EnemySpawner:
    def __init__(self, json_path: str, grarphic_loader, map_w, map_h):

        self._json_path = Path(json_path)
        self._graphic_loader = grarphic_loader
        self._map_w = map_w
        self._map_h = map_h
        #print(f"EnemySpawner initialized with JSON path: {self._json_path}, map width: {self._map_w}, map height: {self._map_h}")

    def load_enemy(self):
        """
        Load an enemy entity with the given parameters.
        """
        with open(self._json_path) as f: 
            enemy_data = json.load(f)
            print(f"Loaded enemy data: {enemy_data}")
        enemies = []
        for config in enemy_data["enemies"]:
            skin_coords = SKIN_REGISTRY.get(config["skin"], ENEMY_DIRECTION_COORDS)
            frames = self._graphic_loader.load_frames(skin_coords)
            enemy = Enemy(
                id=config["id"],
                world_x=config["spawn_x_from_center"],
                world_y=config["spawn_y_from_center"],
                frames=frames
            )
            enemies.append(enemy)
        print(f"Spawned {len(enemies)} enemies from {self._json_path.name}")
        return enemies