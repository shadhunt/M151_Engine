import pygame
from pathlib import Path

from config.analog_control_const import MISSILE_COORDS, PLAYER_DIRECTION_COORDS
from config.properties import *
from config.path_config import *
class GraphicLoader():
    def __init__(self, char_sheet: str | Path = CHAR_SHEET):
        self.sheet = pygame.image.load(char_sheet).convert_alpha()

    def load_frames(self, coord_map: dict) -> dict[str, pygame.Surface]:
        """
        Cut characters.png into one 32×32 Surface per direction.
        Returns a dict: {"up": Surface, "down_right": Surface, ...}
        """       
        frames = {}
        for direction, (row, col) in coord_map.items():
            x, y = char_sheet_cell_position(col, row)
            # Create a blank surface the size of one sprite cell
            frame = pygame.Surface((SPRITE_W, SPRITE_H))
            # create a rect as a "crop window"
            rect = pygame.Rect(x, y, SPRITE_W, SPRITE_H)
            # use the rect(crow window) to cut from the sheet and paste to the top-left corner(0,0) of blank surface
            frame.blit(self.sheet, (0, 0), rect )
            # Mark the cyan color as transparent (colorkey = "treat this color as alpha=0")
            frame.set_colorkey(COLORKEY)
            frames[direction] = frame
        return frames