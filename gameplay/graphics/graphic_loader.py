import pygame
from pathlib import Path

from config.analog_control_const import MISSILE_COORDS, PLAYER_DIRECTION_COORDS
from config.properties import *
from config.path_config import *
class GraphicLoader():
    def __init__(self, char_sheet: str | Path = CHAR_SHEET):
        self.sheet = pygame.image.load(char_sheet).convert_alpha()

    def load_player_frames(self) -> dict[str, pygame.Surface]:
        """
        Cut characters.png into one 32×32 Surface per direction.
        Returns a dict: {"up": Surface, "down_right": Surface, ...}
        """       
        frames = {}
        for direction, (row, col) in PLAYER_DIRECTION_COORDS.items():
            x, y = char_sheet_cell_position(col, row)
            # Create a blank surface the size of one sprite cell
            frame = pygame.Surface((SPRITE_W, SPRITE_H))
            # Copy the correct cell out of the big spritesheet
            # blit(source, dest_pos, source_rect)
            frame.blit(self.sheet, (0, 0), pygame.Rect(x, y, SPRITE_W, SPRITE_H))
            # Mark the cyan color as transparent (colorkey = "treat this color as alpha=0")
            frame.set_colorkey(COLORKEY)
            frames[direction] = frame
        return frames
    def load_missile_frames(self, coord_map: dict = MISSILE_COORDS) -> dict:
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
            x, y = char_sheet_cell_position(col, row)
            rect  = pygame.Rect(x, y, SPRITE_W, SPRITE_H)
            frame = pygame.Surface((SPRITE_W, SPRITE_H))   # plain RGB surface
            frame.blit(self.sheet, (0, 0), rect)           # copy the cell from the sheet
            frame.set_colorkey(COLORKEY)                    # make cyan background transparent
            frames[direction] = frame
        return frames
