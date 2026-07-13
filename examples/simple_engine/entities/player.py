"""
Player -- a keyboard-controlled tank.

Movement lives here; the Animator (see engine/animation.py) just picks
which sprite frame to show for whatever direction we're currently facing.
"""
import pygame

from engine.entity import Entity
from engine.animation import Animator
from engine.input import InputManager
from engine import config


class Player(Entity):
    def __init__(self, entity_id, world_x: float, world_y: float, frames: dict):
        draw_w = config.SPRITE_W * config.PLAYER_SCALE
        draw_h = config.SPRITE_H * config.PLAYER_SCALE
        super().__init__(entity_id, world_x, world_y, draw_w, draw_h)

        self.animator  = Animator(frames, direction=config.DOWN)
        self.direction = config.DOWN
        self.speed     = config.PLAYER_SPEED

    def update(self, dt: float, map_w: int, map_h: int) -> None:
        dx, dy, new_direction = InputManager.read_movement()
        if new_direction is not None:
            self.direction = new_direction
            self.animator.set_direction(new_direction)

        self.world_x += dx * self.speed * dt
        self.world_y += dy * self.speed * dt

        # Clamp to (map_dimension - sprite_dimension), not map_dimension,
        # because world_x/world_y is the sprite's TOP-LEFT corner -- using
        # map_dimension alone would let the right/bottom edge of the
        # sprite hang off the map.
        self.world_x = max(0.0, min(self.world_x, map_w - self.draw_w))
        self.world_y = max(0.0, min(self.world_y, map_h - self.draw_h))

        self.animator.update(dt)

    def draw(self, surface: pygame.Surface, camera) -> None:
        screen_x, screen_y = camera.world_to_screen(self.world_x, self.world_y)
        surface.blit(self.animator.image, (int(screen_x), int(screen_y)))

    def center(self) -> tuple[float, float]:
        """World-space coordinate of the sprite's visual center -- used to
        spawn a missile from the middle of the tank rather than its corner."""
        return self.world_x + self.draw_w / 2, self.world_y + self.draw_h / 2
