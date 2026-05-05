"""
example_missle_shoot.py
=======================

Demonstrates 8-direction missile shooting from a fixed point.

Controls:
  WASD   — change the aim direction (the tank rotates but stays still)
  SPACE  — fire one missile in the current aim direction
  ESC    — quit

──────────────────────────────────────────────────────────────────────────────
HOW THE SPRITESHEET WORKS  (characters.png)
──────────────────────────────────────────────────────────────────────────────

The sheet is one big image divided into a grid of 32×32-pixel cells.
Each cell is separated by a 1-pixel coloured grid line, so:

  cell x-start  =  10  +  col  *  33      ← 10 px left margin, then 33 px steps
  cell y-start  =  25  +  row  *  33      ← 25 px top margin,  then 33 px steps

  (The 33-px step = 32-px sprite + 1-px separator line)

Note: the sheet uses 1-based numbering for rows and columns when you count
visually, but Python arrays are 0-based. So "row 19, col 5" in the art file
means 0-based row 18, col 4 in code.

──────────────────────────────────────────────────────────────────────────────
TANK  (the player)   →   rows 1-2, cols 1-4  (1-based)
                         rows 0-1, cols 0-3  (0-based, used in code)
──────────────────────────────────────────────────────────────────────────────

  Row 0: col0=UP_LEFT  col1=UP   col2=UP_RIGHT  col3=RIGHT
  Row 1: col0=LEFT     col1=DOWN_LEFT  col2=DOWN  col3=DOWN_RIGHT

──────────────────────────────────────────────────────────────────────────────
MISSILE  →   rows 19-20, cols 5-8  (1-based, as given in the art spec)
             rows 18-19, cols 4-7  (0-based, used in code)
──────────────────────────────────────────────────────────────────────────────

  Row 18: col4=UP_LEFT  col5=UP   col6=UP_RIGHT  col7=RIGHT
  Row 19: col4=LEFT     col5=DOWN_LEFT  col6=DOWN  col7=DOWN_RIGHT
"""

import pygame
import sys
from pathlib import Path

# ──────────────────────────────────────────────────────────────────────────────
# PATH SETUP
# ──────────────────────────────────────────────────────────────────────────────
# __file__ is  examples/missle_shoot/example_missle_shoot.py
# .parents[2]  climbs up two directories → M151_Engine root
M151_ROOT = Path(__file__).resolve().parents[2]
SHEET_PATH = M151_ROOT / "assets" / "images" / "characters" / "characters.png"

# ──────────────────────────────────────────────────────────────────────────────
# DIRECTION CONSTANTS
# ──────────────────────────────────────────────────────────────────────────────
UP_LEFT    = "up_left"
UP         = "up"
UP_RIGHT   = "up_right"
RIGHT      = "right"
LEFT       = "left"
DOWN_LEFT  = "down_left"
DOWN       = "down"
DOWN_RIGHT = "down_right"

# ──────────────────────────────────────────────────────────────────────────────
# DISPLAY SETTINGS
# ──────────────────────────────────────────────────────────────────────────────
WINDOW_W   = 800
WINDOW_H   = 600
FPS        = 60
BG_COLOR   = (30, 30, 50)         # dark navy background
SCALE      = 3                    # every 32-px sprite becomes 96×96 on screen

# ──────────────────────────────────────────────────────────────────────────────
# SPRITESHEET SETTINGS
# ──────────────────────────────────────────────────────────────────────────────
SPRITE_W = SPRITE_H = 32
TRANSPARENT_COLOR   = (32, 200, 248)   # cyan grid background → made transparent

def cell_x(col_0based: int) -> int:
    """Return the pixel x-start of a 0-based column in the spritesheet."""
    return 10 + col_0based * 33

def cell_y(row_0based: int) -> int:
    """Return the pixel y-start of a 0-based row in the spritesheet."""
    return 25 + row_0based * 33


# ──────────────────────────────────────────────────────────────────────────────
# SPRITE COORDINATE MAPS
# Each entry: direction → (0-based row, 0-based col) in the spritesheet
# ──────────────────────────────────────────────────────────────────────────────

# Tank (player) — rows 0-1, cols 0-3 (0-based)
TANK_COORDS = {
    UP_LEFT:    (0, 0),
    UP:         (0, 1),
    UP_RIGHT:   (0, 2),
    RIGHT:      (0, 3),
    LEFT:       (1, 0),
    DOWN_LEFT:  (1, 1),
    DOWN:       (1, 2),
    DOWN_RIGHT: (1, 3),
}

# Missile — rows 18-19, cols 4-7 (0-based)  ←  art-file rows 19-20, cols 5-8 (1-based)
MISSILE_COORDS = {
    UP_LEFT:    (18, 4),
    UP:         (18, 5),
    UP_RIGHT:   (18, 6),
    RIGHT:      (18, 7),
    LEFT:       (19, 4),
    DOWN_LEFT:  (19, 5),
    DOWN:       (19, 6),
    DOWN_RIGHT: (19, 7),
}


def load_frames(sheet: pygame.Surface, coord_map: dict) -> dict:
    """
    Cut every sprite out of `sheet` according to `coord_map` and return
    a dict of { direction_string → pygame.Surface (32×32, transparent bg) }.

    Why set_colorkey instead of SRCALPHA?
      The spritesheet was saved without an alpha channel, so each cell has a
      solid cyan background (32, 200, 248).  set_colorkey tells pygame to treat
      that exact colour as fully transparent when blitting — no alpha channel needed.
    """
    frames = {}
    for direction, (row, col) in coord_map.items():
        x = cell_x(col)
        y = cell_y(row)
        rect  = pygame.Rect(x, y, SPRITE_W, SPRITE_H)
        frame = pygame.Surface((SPRITE_W, SPRITE_H))   # plain RGB surface
        frame.blit(sheet, (0, 0), rect)                # copy the cell from the sheet
        frame.set_colorkey(TRANSPARENT_COLOR)           # make cyan → transparent
        frames[direction] = frame
    return frames


# ──────────────────────────────────────────────────────────────────────────────
# MISSILE PHYSICS
# ──────────────────────────────────────────────────────────────────────────────
MISSILE_SPEED = 450    # pixels per second for cardinal directions

_S = MISSILE_SPEED
_D = MISSILE_SPEED * 0.707   # diagonal speed: same actual distance per second
                              # as cardinal (multiply by 1/√2 to normalise)

# velocity (vx, vy) in pixels-per-second for each direction
VELOCITY_MAP = {
    UP:         ( 0,  -_S),
    DOWN:       ( 0,  +_S),
    LEFT:       (-_S,  0),
    RIGHT:      (+_S,  0),
    UP_LEFT:    (-_D, -_D),
    UP_RIGHT:   (+_D, -_D),
    DOWN_LEFT:  (-_D, +_D),
    DOWN_RIGHT: (+_D, +_D),
}


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

    def __init__(self, x: float, y: float, direction: str, frames: dict, scale: int):
        self.x = x
        self.y = y
        self.vx, self.vy = VELOCITY_MAP[direction]

        # Pre-scale the sprite once at creation so we don't rescale every frame.
        raw = frames[direction]
        self.image = pygame.transform.scale(raw, (SPRITE_W * scale, SPRITE_H * scale))
        self.size  = SPRITE_W * scale   # we'll use this for off-screen detection

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


# ──────────────────────────────────────────────────────────────────────────────
# DIRECTION SELECTION (keyboard → aim)
# ──────────────────────────────────────────────────────────────────────────────

def get_aim_direction(current_direction: str) -> str:
    """
    Read WASD keys and return the aimed direction.
    If no key is pressed (or opposing keys cancel), keep the current direction.

    This is checked with pygame.key.get_pressed() — it reads the keyboard
    state every frame, so holding a key is smooth with no OS repeat-delay.
    """
    keys  = pygame.key.get_pressed()
    up    = keys[pygame.K_w]
    down  = keys[pygame.K_s]
    left  = keys[pygame.K_a]
    right = keys[pygame.K_d]

    match (up, down, left, right):
        case (True,  False, True,  False): return UP_LEFT
        case (True,  False, False, True):  return UP_RIGHT
        case (False, True,  True,  False): return DOWN_LEFT
        case (False, True,  False, True):  return DOWN_RIGHT
        case (True,  False, False, False): return UP
        case (False, True,  False, False): return DOWN
        case (False, False, True,  False): return LEFT
        case (False, False, False, True):  return RIGHT
        case _:                            return current_direction  # no change


# ──────────────────────────────────────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_W, WINDOW_H), pygame.RESIZABLE)
    pygame.display.set_caption("M151 Engine — Missile Shoot Example")
    clock = pygame.time.Clock()
    font  = pygame.font.Font(None, 26)

    # Load the spritesheet once, then cut all frames from it
    sheet          = pygame.image.load(SHEET_PATH).convert_alpha()
    tank_frames    = load_frames(sheet, TANK_COORDS)
    missile_frames = load_frames(sheet, MISSILE_COORDS)

    # Pre-scale tank sprites (done once, not every frame)
    tank_scaled = {
        direction: pygame.transform.scale(surf, (SPRITE_W * SCALE, SPRITE_H * SCALE))
        for direction, surf in tank_frames.items()
    }

    # ── Tank is fixed at the centre of the window ──
    tank_w = tank_h = SPRITE_W * SCALE
    tank_x = WINDOW_W // 2 - tank_w // 2
    tank_y = WINDOW_H // 2 - tank_h // 2

    aim_direction: str  = UP          # which way the tank is currently facing
    missiles: list[Missile] = []

    running = True
    while running:

        # delta-time: how many seconds since the last frame.
        # Capping at 60 FPS means dt is at most 1/60 ≈ 0.0167 s.
        # All movement is multiplied by dt so the game runs at the same
        # speed regardless of frame rate.
        dt = clock.tick(FPS) / 1000.0

        # ── Event loop ────────────────────────────────────────────────────────
        # KEYDOWN fires once per physical key press (not while held).
        # That's why we use it for shooting — one press = one missile.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                if event.key == pygame.K_SPACE:
                    # Spawn the missile at the tank's centre so it appears to
                    # come from the middle of the sprite, not the top-left corner.
                    missile_size = SPRITE_W * SCALE
                    mx = tank_x + tank_w // 2 - missile_size // 2
                    my = tank_y + tank_h // 2 - missile_size // 2
                    missiles.append(Missile(mx, my, aim_direction, missile_frames, SCALE))

        # ── Update aim direction (held keys, checked every frame) ─────────────
        aim_direction = get_aim_direction(aim_direction)

        # ── Update missiles ───────────────────────────────────────────────────
        for m in missiles:
            m.update(dt)

        # Remove missiles that have fully left the screen.
        # List comprehension builds a new list keeping only the ones still on screen.
        missiles = [m for m in missiles if not m.is_offscreen(WINDOW_W, WINDOW_H)]

        # ── Draw ──────────────────────────────────────────────────────────────
        screen.fill(BG_COLOR)

        # Draw missiles first so they appear under the tank
        for m in missiles:
            m.draw(screen)

        # Draw the tank on top
        screen.blit(tank_scaled[aim_direction], (tank_x, tank_y))

        # HUD text
        hud_lines = [
            "WASD: aim direction   SPACE: fire   ESC: quit",
            f"Aim: {aim_direction:<12}   Missiles in flight: {len(missiles)}",
        ]
        for i, line in enumerate(hud_lines):
            text_surf = font.render(line, True, (210, 210, 210))
            screen.blit(text_surf, (10, 10 + i * 28))

        pygame.display.flip()

    pygame.quit()
    sys.exit()
