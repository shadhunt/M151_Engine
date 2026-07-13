"""
Missile -- now a full Entity. Earlier M151_Engine prototypes kept
Missile outside the Entity hierarchy even though it has the exact same
world_x/world_y/update/draw shape; being an Entity here means it plugs
into EntityManager and CollisionSystem for free, with no special-casing.
"""
import pygame

from engine.entity import Entity
from engine import config

_VELOCITY_BY_DIRECTION = {
    config.UP:         (0.0, -config.MISSILE_SPEED),
    config.DOWN:       (0.0,  config.MISSILE_SPEED),
    config.LEFT:       (-config.MISSILE_SPEED, 0.0),
    config.RIGHT:      ( config.MISSILE_SPEED, 0.0),
    config.UP_LEFT:    (-config.MISSILE_SPEED * 0.707, -config.MISSILE_SPEED * 0.707),
    config.UP_RIGHT:   ( config.MISSILE_SPEED * 0.707, -config.MISSILE_SPEED * 0.707),
    config.DOWN_LEFT:  (-config.MISSILE_SPEED * 0.707,  config.MISSILE_SPEED * 0.707),
    config.DOWN_RIGHT: ( config.MISSILE_SPEED * 0.707,  config.MISSILE_SPEED * 0.707),
}


class Missile(Entity):
    def __init__(self, entity_id, world_x: float, world_y: float, direction: str, image: pygame.Surface):
        size = config.SPRITE_W * config.MISSILE_SCALE
        super().__init__(entity_id, world_x, world_y, size, size)
        self.vx, self.vy = _VELOCITY_BY_DIRECTION[direction]
        self.image = image

    def update(self, dt: float, map_w: int, map_h: int) -> None:
        self.world_x += self.vx * dt
        self.world_y += self.vy * dt

        # Kill once fully off the MAP (not just the camera's current
        # view) -- simplest correct bound for a demo this size. A
        # view-only check would also need the camera passed in here.
        if (self.world_x + self.draw_w < 0 or self.world_x > map_w or
                self.world_y + self.draw_h < 0 or self.world_y > map_h):
            self.kill()

    def draw(self, surface: pygame.Surface, camera) -> None:
        screen_x, screen_y = camera.world_to_screen(self.world_x, self.world_y)
        surface.blit(self.image, (int(screen_x), int(screen_y)))
