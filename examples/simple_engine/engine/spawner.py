"""
JSONSpawner -- reads a JSON file of entity specs and turns each one into
a live entity via a factory function you provide.

This generalizes the ad hoc EnemySpawner from
examples/enemies_spawner/spawner-example.py: the factory indirection
means the SAME spawner class can spawn enemies, pickups, or anything
else you invent later, as long as you give it a function that builds one
entity from a spec dict.
"""
import json
from pathlib import Path


class JSONSpawner:
    def __init__(self, json_path, map_w: int, map_h: int):
        self._json_path = Path(json_path)
        self._map_w = map_w
        self._map_h = map_h

    def load(self, key: str, factory) -> list:
        """
        key:     top-level JSON array to read (e.g. "enemies")
        factory: function(spec: dict, world_x: float, world_y: float) -> Entity

        Spawn positions in the JSON are offsets from the map's CENTER
        (spawn_x_from_center / spawn_y_from_center) rather than absolute
        pixels, so the same file still works if you swap in a
        differently-sized map image.
        """
        with open(self._json_path) as f:
            data = json.load(f)

        spawned = []
        for spec in data.get(key, []):
            world_x = self._map_w / 2 + spec.get("spawn_x_from_center", 0)
            world_y = self._map_h / 2 + spec.get("spawn_y_from_center", 0)
            spawned.append(factory(spec, world_x, world_y))
        return spawned
