import pygame
import sys
from pathlib import Path

FRAMEWORK_ROOT = str( Path(__file__).resolve().parents[1])    # set parents level to 2 if want to run in template folder directly, otherwise, set to 1
sys.path.append(FRAMEWORK_ROOT)

from config.analog_control_const import PLAYER_DIRECTION_COORDS
from config.properties import *
from config.path_config import *
class GraphicLoader():
    def __init__(self):
        self.frames = pygame.image.load(CHAR_SHEET).convert_alpha()
        
    def load_player_frames(self, char_sheet: str | Path) -> dict[str, pygame.Surface]:
        """
        Cut characters.png into one 32×32 Surface per direction.
        Returns a dict: {"up": Surface, "down_right": Surface, ...}
        """       
        frames = {}
        for direction, (row, col) in PLAYER_DIRECTION_COORDS.items():
            # Create a blank surface the size of one sprite cell
            frame = pygame.Surface((SPRITE_W, SPRITE_H))
            # Copy the correct cell out of the big spritesheet
            # blit(source, dest_pos, source_rect)
            frame.blit(self.frames, (0, 0), pygame.Rect(PLAYER_COL_X[col], PLAYER_ROW_Y[row], SPRITE_W, SPRITE_H))
            # Mark the cyan color as transparent (colorkey = "treat this color as alpha=0")
            frame.set_colorkey(COLORKEY)
            frames[direction] = frame
        return frames
    def load_missile_frames(sheet: pygame.Surface, coord_map: dict) -> dict:
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