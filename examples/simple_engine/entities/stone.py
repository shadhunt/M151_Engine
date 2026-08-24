import pygame

from engine.entity import Entity


class Stone(Entity):
    def __init__(self, entity_id, world_x: float, world_y: float, width: int, height: int):
        super().__init__(entity_id, world_x, world_y, width, height)
    def update(self, dt: float, map_w: int, map_h: int) -> None:
        pass
    def draw(self, surface: pygame.Surface, camera) -> None:
        pass