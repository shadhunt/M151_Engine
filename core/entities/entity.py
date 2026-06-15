import pygame
from config.properties import *
from utils.keyboard_controller import KeyboardController

DEBUG = True
class Entity:
    """
    An entity exists in WORLD SPACE.

    world_x and world_y are its position on the full game map.
    They have nothing to do with where the sprite appears on screen —
    that conversion is done externally by the Camera.

    Keeping world position and screen position strictly separate is what
    makes the camera system work. The entity never needs to know about
    the camera, and the camera never needs to know about gameplay logic.
    """
    id: int
    world_x: float
    world_y: float
    direction: str
    SPEED = 220   # pixels per second in world space

    def __init__( self, id, world_x: float, world_y: float, frames: dict):
        if DEBUG:
            print(world_x, world_y)
        self.id = id
        self.world_x   = float(world_x)
        self.world_y   = float(world_y)
        self.direction = "up"   # facing direction, used to pick the sprite frame
        self.frames    = frames

        # Scale up for visibility: 32×32 px is tiny on a modern screen
        self.scale  = 4
        self.draw_w = SPRITE_W * self.scale   # 128 px
        self.draw_h = SPRITE_H * self.scale   # 128 px

        '''
        That's a dictionary comprehension — a concise way to build a dictionary in one expression.

        The general syntax is:
        {key_expr: value_expr for key, value in iterable}

        Breaking down your example:
        self._scaled_frames = {
            d: pygame.transform.scale(f, (self.draw_w, self.draw_h))
            for d, f in frames.items()
        }

        - frames.items() yields (key, value) pairs from the frames dict
        - Each pair is unpacked into d (direction/key) and f (frame/value)
        - For every pair, it creates a new entry: d as the key, scaled version of f as the value

        It's equivalent to this loop:
        self._scaled_frames = {}
        for d, f in frames.items():
            self._scaled_frames[d] = pygame.transform.scale(f, (self.draw_w, self.draw_h))

        The comprehension version is just more Pythonic and compact. You'll also see the same pattern for lists ([x for x in ...]) and sets ({x for x in ...})
        '''
        self._scaled_frames = { d: pygame.transform.scale(f, (self.draw_w, self.draw_h)) for d, f in frames.items()}


    def update(self, dt: float, map_w: int, map_h: int) -> None:
        """
        Read input, move in world space, clamp to map boundaries.

        DELTA-TIME (dt):
            dt = seconds elapsed since the previous frame.
            At 60 fps → dt ≈ 0.0167 s  →  220 * 0.0167 ≈  3.7 px per frame
            At 30 fps → dt ≈ 0.0333 s  →  220 * 0.0333 ≈  7.3 px per frame

            Either way, over one full second the entity travels 220 pixels.
            Without dt the entity would move faster on faster hardware.

        MAP BOUNDARY CLAMP:
            Ensure the sprite stays fully inside the map.
            The upper limit is (map_dimension - sprite_dimension) rather than
            map_dimension alone, because (world_x, world_y) is the sprite's
            TOP-LEFT corner — if we clamped to map_w the right edge of the
            sprite would extend 128 px past the map boundary.
        """
        dx, dy, new_dir = KeyboardController.read_keys()        
        if new_dir is not None:
            self.direction = new_dir

        self.world_x += dx * self.SPEED * dt
        self.world_y += dy * self.SPEED * dt

        # Clamp: keep the sprite fully inside the map
        self.world_x = max(0.0, min(self.world_x, map_w - self.draw_w))
        self.world_y = max(0.0, min(self.world_y, map_h - self.draw_h))

    def draw(self, screen: pygame.Surface, screen_x: float, screen_y: float) -> None:
        """
        Draw the sprite at (screen_x, screen_y) — NOT at world_x / world_y.

        The caller computes (screen_x, screen_y) via Camera.world_to_screen()
        before calling this method. The entity itself has no knowledge of
        the camera — it just accepts the screen position and draws there.
        """
        if DEBUG:
            print("draw:",screen_x, screen_y)
        screen.blit(self._scaled_frames[self.direction],(int(screen_x),int(screen_y)))

    def __del__(self):
        if DEBUG:
            print("Entity %d destroyed!!", self.id)