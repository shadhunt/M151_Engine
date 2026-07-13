"""
Engine-wide constants for the Simple Engine example.

Keeping every "magic number" in one place means changing the screen
resolution, sprite scale, or sheet layout never requires hunting through
gameplay code to find where it's hardcoded.
"""
from pathlib import Path

# ── Paths ────────────────────────────────────────────────────────────────────
ROOT_DIR   = Path(__file__).resolve().parent.parent      # .../simple_engine
ASSETS_DIR = ROOT_DIR / "assets"
DATA_DIR   = ROOT_DIR / "data"

CHAR_SHEET   = ASSETS_DIR / "images" / "characters" / "characters.png"
MAP_IMAGE    = ASSETS_DIR / "images" / "map" / "m151_practice_stage.png"
ENEMIES_JSON = DATA_DIR / "enemies.json"

# ── Display ──────────────────────────────────────────────────────────────────
SCREEN_W = 960
SCREEN_H = 540
FPS      = 60
TITLE    = "M151 Simple Engine -- Demo"

# ── Sprite sheet grid (characters.png) ───────────────────────────────────────
# The sheet is a grid of 32x32 cells separated by 1px lines.
# Column content starts at x=10, row content starts at y=25; both repeat
# every 33px (32px cell + 1px separator). See ResourceLoader.cell_position().
SPRITE_W = 32
SPRITE_H = 32
SHEET_COL_START_X = 10
SHEET_ROW_START_Y = 25
SHEET_CELL_PITCH  = 33

COLORKEY = (32, 200, 248)   # cyan in the source art -> treated as transparent

# ── Gameplay tuning ───────────────────────────────────────────────────────────
PLAYER_SCALE = 4
PLAYER_SPEED = 220           # world pixels / second

ENEMY_SCALE = 3
ENEMY_SPEED = 180

MISSILE_SCALE = 4
MISSILE_SPEED = 1100

# ── Direction constants ───────────────────────────────────────────────────────
UP, DOWN, LEFT, RIGHT = "up", "down", "left", "right"
UP_LEFT, UP_RIGHT     = "up_left", "up_right"
DOWN_LEFT, DOWN_RIGHT = "down_left", "down_right"

# Row/col of each direction inside characters.png.
# Rows 0-1 are the player skin, rows 6-7 the enemy skin, rows 18-19 the missile.
PLAYER_SHEET_COORDS = {
    UP_LEFT: (0, 0), UP: (0, 1), UP_RIGHT: (0, 2), RIGHT: (0, 3),
    LEFT: (1, 0), DOWN_LEFT: (1, 1), DOWN: (1, 2), DOWN_RIGHT: (1, 3),
}
ENEMY_SHEET_COORDS = {
    UP_LEFT: (6, 0), UP: (6, 1), UP_RIGHT: (6, 2), RIGHT: (6, 3),
    LEFT: (7, 0), DOWN_LEFT: (7, 1), DOWN: (7, 2), DOWN_RIGHT: (7, 3),
}
MISSILE_SHEET_COORDS = {
    UP_LEFT: (18, 4), UP: (18, 5), UP_RIGHT: (18, 6), RIGHT: (18, 7),
    LEFT: (19, 4), DOWN_LEFT: (19, 5), DOWN: (19, 6), DOWN_RIGHT: (19, 7),
}

ENEMY_PATROL_PATH = [RIGHT, DOWN_RIGHT, DOWN, DOWN_LEFT, LEFT, UP_LEFT, UP, UP_RIGHT]
