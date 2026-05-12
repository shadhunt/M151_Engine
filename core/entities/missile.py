import pygame
from config.properties import SCALE, SPRITE_W, SPRITE_H
from config.analog_control_const import VELOCITY_MAP

class Missile:
    """
    One missile travelling across the screen.

    Position is stored as floats so sub-pixel movement stays accurate
    even at high speed.  We only round to int when drawing.

    Lifecycle:
      1. Created at the tank's centre when SPACE is pressed.
      2. Updated every frame: position += velocity * dt.
      3. Removed from the list once it fully exits the window.
    """
    size = SPRITE_W * SCALE
    half_size = size // 2

    def __init__(self, x: float, y: float, direction: str, frames: dict):
        self.x = x
        self.y = y
        sheet = pygame.image.load(SHEET_PATH).convert_alpha()
        self.missile_frames = load_frames(sheet, MISSILE_COORDS)
        self.vx, self.vy = VELOCITY_MAP[direction]

        # Pre-scale the sprite once at creation so we don't rescale every frame.
        raw = frames[direction]
        self.image = pygame.transform.scale(raw, (SPRITE_W * SCALE, SPRITE_H * SCALE))
        self.size  = SPRITE_W * SCALE   # we'll use this for off-screen detection

    def update(self, dt: float):
        """Move by velocity × elapsed seconds (frame-rate-independent)."""
        self.x += self.vx * dt
        self.y += self.vy * dt

    def is_offscreen(self, screen_w: int, screen_h: int) -> bool:
        """True once the entire sprite has left the visible area."""
        return (self.x + self.size < 0 or self.x > screen_w or
                self.y + self.size < 0 or self.y > screen_h)

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, (int(self.x), int(self.y)))
