import math
import sys
from pathlib import Path

import pygame


M151_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(M151_ROOT))

from config.path_config import CHAR_SHEET
from config.properties import COLORKEY, SPRITE_H, SPRITE_W, char_sheet_cell_position


SCREEN_SIZE = (960, 540)
FPS = 60
ENEMY_SCALE = 3
ENEMY_SPEED = 180

UP_LEFT = "up_left"
UP = "up"
UP_RIGHT = "up_right"
RIGHT = "right"
LEFT = "left"
DOWN_LEFT = "down_left"
DOWN = "down"
DOWN_RIGHT = "down_right"

ENEMY_DIRECTION_COORDS = {
    UP_LEFT: (6, 0),
    UP: (6, 1),
    UP_RIGHT: (6, 2),
    RIGHT: (6, 3),
    LEFT: (7, 0),
    DOWN_LEFT: (7, 1),
    DOWN: (7, 2),
    DOWN_RIGHT: (7, 3),
}

ENEMY_PATH = [
    RIGHT,
    DOWN_RIGHT,
    DOWN,
    DOWN_LEFT,
    LEFT,
    UP_LEFT,
    UP,
    UP_RIGHT,
]

VELOCITY = {
    UP: (0, -1),
    DOWN: (0, 1),
    LEFT: (-1, 0),
    RIGHT: (1, 0),
    UP_LEFT: (-1, -1),
    UP_RIGHT: (1, -1),
    DOWN_LEFT: (-1, 1),
    DOWN_RIGHT: (1, 1),
}


def load_enemy_frames() -> dict[str, pygame.Surface]:
    sheet = pygame.image.load(CHAR_SHEET).convert_alpha()
    frames = {}

    for direction, (sheet_row, sheet_col) in ENEMY_DIRECTION_COORDS.items():
        x, y = char_sheet_cell_position(sheet_col, sheet_row)
        rect = pygame.Rect(x, y, SPRITE_W, SPRITE_H)
        frame = pygame.Surface((SPRITE_W, SPRITE_H))
        frame.blit(sheet, (0, 0), rect)
        frame.set_colorkey(COLORKEY)
        frames[direction] = pygame.transform.scale(
            frame,
            (SPRITE_W * ENEMY_SCALE, SPRITE_H * ENEMY_SCALE),
        )

    return frames


class Enemy:
    def __init__(self, frames: dict[str, pygame.Surface], screen_rect: pygame.Rect):
        self.frames = frames
        self.direction_index = 0
        self.direction = ENEMY_PATH[self.direction_index]
        self.image = self.frames[self.direction]
        self.rect = self.image.get_rect(center=screen_rect.center)
        self.change_timer = 0.0
        self.change_every = 0.85

    def update(self, dt: float, bounds: pygame.Rect) -> None:
        self.change_timer += dt
        if self.change_timer >= self.change_every:
            self.change_timer = 0.0
            self.direction_index = (self.direction_index + 1) % len(ENEMY_PATH)
            self.direction = ENEMY_PATH[self.direction_index]
            self.image = self.frames[self.direction]

        vx, vy = VELOCITY[self.direction]
        if vx and vy:
            vx /= math.sqrt(2)
            vy /= math.sqrt(2)

        self.rect.x += round(vx * ENEMY_SPEED * dt)
        self.rect.y += round(vy * ENEMY_SPEED * dt)

        if self.rect.left < bounds.left:
            self.rect.left = bounds.left
            self._face(RIGHT)
        elif self.rect.right > bounds.right:
            self.rect.right = bounds.right
            self._face(LEFT)

        if self.rect.top < bounds.top:
            self.rect.top = bounds.top
            self._face(DOWN)
        elif self.rect.bottom > bounds.bottom:
            self.rect.bottom = bounds.bottom
            self._face(UP)

    def _face(self, direction: str) -> None:
        self.direction = direction
        self.direction_index = ENEMY_PATH.index(direction)
        self.image = self.frames[self.direction]
        self.change_timer = 0.0

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.image, self.rect)


def draw_background(surface: pygame.Surface) -> None:
    surface.fill((34, 37, 42))
    for x in range(0, surface.get_width(), 48):
        pygame.draw.line(surface, (45, 49, 55), (x, 0), (x, surface.get_height()))
    for y in range(0, surface.get_height(), 48):
        pygame.draw.line(surface, (45, 49, 55), (0, y), (surface.get_width(), y))


def main() -> None:
    pygame.init()
    pygame.display.set_caption("M151 Enemy Move Example")
    screen = pygame.display.set_mode(SCREEN_SIZE, pygame.RESIZABLE)
    clock = pygame.time.Clock()

    enemy = Enemy(load_enemy_frames(), screen.get_rect().inflate(-80, -80))
    running = True

    while running:
        dt = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        bounds = screen.get_rect().inflate(-80, -80)
        enemy.update(dt, bounds)

        draw_background(screen)
        pygame.draw.rect(screen, (75, 83, 94), bounds, 1)
        enemy.draw(screen)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
