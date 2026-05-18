import pygame
from config.analog_control_const import *
from config.properties import *

class Enemy:
    def __init__(self, world_x: float, world_y: float, frames: dict[str, pygame.Surface]):
        self.world_x = float(world_x)
        self.world_y = float(world_y)
        self.frames = frames
        self.direction_index = 0
        self.direction = ENEMY_PATH[self.direction_index]
        self.scale = ENEMY_SCALE
        self.draw_w = SPRITE_W * self.scale
        self.draw_h = SPRITE_H * self.scale
        self._scaled_frames = {
            direction: pygame.transform.scale(frame, (self.draw_w, self.draw_h))
            for direction, frame in frames.items()
        }
        self.image = self._scaled_frames[self.direction]
        self.change_timer = 0.0
        self.change_every = 0.85

    def update(self, dt: float, map_w: int, map_h: int) -> None:
        self.change_timer += dt
        if self.change_timer >= self.change_every:
            self.change_timer = 0.0
            self.direction_index = (self.direction_index + 1) % len(ENEMY_PATH)
            self.direction = ENEMY_PATH[self.direction_index]
            self.image = self._scaled_frames[self.direction]

        vx, vy = self._direction_vector()
        self.world_x += vx * ENEMY_SPEED * dt
        self.world_y += vy * ENEMY_SPEED * dt

        if self.world_x < 0:
            self.world_x = 0
            self._face(RIGHT)
        elif self.world_x > map_w - self.draw_w:
            self.world_x = map_w - self.draw_w
            self._face(LEFT)

        if self.world_y < 0:
            self.world_y = 0
            self._face(DOWN)
        elif self.world_y > map_h - self.draw_h:
            self.world_y = map_h - self.draw_h
            self._face(UP)

    def _direction_vector(self) -> tuple[float, float]:
        if self.direction == UP:
            return 0.0, -1.0
        if self.direction == DOWN:
            return 0.0, 1.0
        if self.direction == LEFT:
            return -1.0, 0.0
        if self.direction == RIGHT:
            return 1.0, 0.0
        if self.direction == UP_LEFT:
            return -0.707, -0.707
        if self.direction == UP_RIGHT:
            return 0.707, -0.707
        if self.direction == DOWN_LEFT:
            return -0.707, 0.707
        return 0.707, 0.707

    def _face(self, direction: str) -> None:
        self.direction = direction
        self.direction_index = ENEMY_PATH.index(direction)
        self.image = self._scaled_frames[self.direction]
        self.change_timer = 0.0

    def draw(self, surface: pygame.Surface, screen_x: float, screen_y: float) -> None:
        surface.blit(self.image, (int(screen_x), int(screen_y)))
