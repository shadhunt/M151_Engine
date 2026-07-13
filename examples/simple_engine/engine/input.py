"""
InputManager -- polls WASD every frame and returns a normalized movement
vector plus the direction name to show on the sprite.

See "Chapter 3 -- Input & Direction Normalization" in the PDF guide for
the full derivation of why diagonal movement gets multiplied by 0.707.
"""
import pygame

from . import config

DIAGONAL_FACTOR = 0.70710678   # 1/sqrt(2) -- keeps diagonal speed equal to cardinal speed


class InputManager:
    @staticmethod
    def read_movement() -> tuple[float, float, str | None]:
        keys  = pygame.key.get_pressed()
        up    = keys[pygame.K_w]
        down  = keys[pygame.K_s]
        left  = keys[pygame.K_a]
        right = keys[pygame.K_d]

        d = DIAGONAL_FACTOR
        # Matching on the 4-key tuple covers all 8 directions in one place;
        # opposing keys (e.g. W+S) fall through to "no movement".
        match (up, down, left, right):
            case (True,  False, True,  False): return (-d, -d, config.UP_LEFT)
            case (True,  False, False, True):  return ( d, -d, config.UP_RIGHT)
            case (False, True,  True,  False): return (-d,  d, config.DOWN_LEFT)
            case (False, True,  False, True):  return ( d,  d, config.DOWN_RIGHT)
            case (True,  False, False, False): return (0.0, -1.0, config.UP)
            case (False, True,  False, False): return (0.0,  1.0, config.DOWN)
            case (False, False, True,  False): return (-1.0, 0.0, config.LEFT)
            case (False, False, False, True):  return ( 1.0, 0.0, config.RIGHT)
            case _:                            return (0.0, 0.0, None)
