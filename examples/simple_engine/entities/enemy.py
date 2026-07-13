"""
Enemy -- position, sprite, speed, and movement "trail" all come from a
JSON spec (see data/enemies.json) rather than being hardcoded.

Three trail styles are implemented below. Adding a fourth means adding
one more _update_x method and one branch in update() -- nothing in
PlayScene, EntityManager, or CollisionSystem has to change.
"""
import pygame

from engine.entity import Entity
from engine.animation import Animator
from engine import config

_DIRECTION_VECTORS = {
    config.UP: (0.0, -1.0), config.DOWN: (0.0, 1.0),
    config.LEFT: (-1.0, 0.0), config.RIGHT: (1.0, 0.0),
    config.UP_LEFT: (-0.707, -0.707), config.UP_RIGHT: (0.707, -0.707),
    config.DOWN_LEFT: (-0.707, 0.707), config.DOWN_RIGHT: (0.707, 0.707),
}


def _direction_from_signs(vx: float, vy: float) -> str:
    if vx > 0 and vy < 0: return config.UP_RIGHT
    if vx < 0 and vy < 0: return config.UP_LEFT
    if vx > 0 and vy > 0: return config.DOWN_RIGHT
    if vx < 0 and vy > 0: return config.DOWN_LEFT
    if vx > 0: return config.RIGHT
    if vx < 0: return config.LEFT
    return config.DOWN if vy > 0 else config.UP


class Enemy(Entity):
    def __init__(self, entity_id, world_x: float, world_y: float, frames: dict,
                 trail: str = "patrol", speed: float = config.ENEMY_SPEED):
        draw_w = config.SPRITE_W * config.ENEMY_SCALE
        draw_h = config.SPRITE_H * config.ENEMY_SCALE
        super().__init__(entity_id, world_x, world_y, draw_w, draw_h)

        self.animator = Animator(frames, direction=config.RIGHT)
        self.trail    = trail
        self.speed    = speed

        # -- patrol state --
        self._patrol_index = 0
        self._patrol_timer = 0.0
        self._patrol_every = 1.85   # seconds between direction changes

        # -- bounce state: signs (+1/-1) of the diagonal velocity --
        self._bounce_vx = 1.0
        self._bounce_vy = 1.0

        # -- zigzag state: alternating horizontal/vertical legs --
        self._zigzag_phase = 0            # 0 = horizontal leg, 1 = vertical leg
        self._zigzag_timer = 0.0
        self._zigzag_switch_every = 1.5   # seconds per leg
        self._zigzag_sign = 1.0

    def update(self, dt: float, map_w: int, map_h: int) -> None:
        if self.trail == "bounce":
            self._update_bounce(dt, map_w, map_h)
        elif self.trail == "zigzag":
            self._update_zigzag(dt, map_w, map_h)
        else:
            self._update_patrol(dt, map_w, map_h)
        self.animator.update(dt)

    def draw(self, surface: pygame.Surface, camera) -> None:
        screen_x, screen_y = camera.world_to_screen(self.world_x, self.world_y)
        surface.blit(self.animator.image, (int(screen_x), int(screen_y)))

    # ── trail implementations ────────────────────────────────────────────

    def _update_patrol(self, dt, map_w, map_h):
        """Rotate through all 8 compass directions on a fixed timer."""
        self._patrol_timer += dt
        if self._patrol_timer >= self._patrol_every:
            self._patrol_timer = 0.0
            self._patrol_index = (self._patrol_index + 1) % len(config.ENEMY_PATROL_PATH)
            self.animator.set_direction(config.ENEMY_PATROL_PATH[self._patrol_index])

        vx, vy = _DIRECTION_VECTORS[self.animator.direction]
        self.world_x += vx * self.speed * dt
        self.world_y += vy * self.speed * dt
        self._clamp(map_w, map_h)

    def _update_bounce(self, dt, map_w, map_h):
        """Billiard-ball diagonal bounce off the map edges."""
        self.world_x += self._bounce_vx * self.speed * dt
        self.world_y += self._bounce_vy * self.speed * dt

        if self.world_x <= 0:
            self.world_x, self._bounce_vx = 0.0, 1.0
        elif self.world_x >= map_w - self.draw_w:
            self.world_x, self._bounce_vx = float(map_w - self.draw_w), -1.0

        if self.world_y <= 0:
            self.world_y, self._bounce_vy = 0.0, 1.0
        elif self.world_y >= map_h - self.draw_h:
            self.world_y, self._bounce_vy = float(map_h - self.draw_h), -1.0

        self.animator.set_direction(_direction_from_signs(self._bounce_vx, self._bounce_vy))

    def _update_zigzag(self, dt, map_w, map_h):
        """Alternate horizontal/vertical legs every N seconds -- an L-shaped path."""
        self._zigzag_timer += dt
        if self._zigzag_timer >= self._zigzag_switch_every:
            self._zigzag_timer = 0.0
            self._zigzag_phase = 1 - self._zigzag_phase

        if self._zigzag_phase == 0:
            self.world_x += self._zigzag_sign * self.speed * dt
            if self.world_x <= 0 or self.world_x >= map_w - self.draw_w:
                self._zigzag_sign *= -1
            self.animator.set_direction(config.RIGHT if self._zigzag_sign > 0 else config.LEFT)
        else:
            self.world_y += self._zigzag_sign * self.speed * dt
            if self.world_y <= 0 or self.world_y >= map_h - self.draw_h:
                self._zigzag_sign *= -1
            self.animator.set_direction(config.DOWN if self._zigzag_sign > 0 else config.UP)

        self._clamp(map_w, map_h)

    def _clamp(self, map_w, map_h):
        self.world_x = max(0.0, min(self.world_x, map_w - self.draw_w))
        self.world_y = max(0.0, min(self.world_y, map_h - self.draw_h))
