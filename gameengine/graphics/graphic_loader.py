import pygame
import sys
from pathlib import Path

FRAMEWORK_ROOT = str( Path(__file__).resolve().parents[1])    # set parents level to 2 if want to run in template folder directly, otherwise, set to 1
sys.path.append(FRAMEWORK_ROOT)

from config.analog_control_const import DIRECTION_COORDS
from config.properties import *

class GraphicLoader():
    @staticmethod
    def load_frames(char_sheet: str | Path) -> dict[str, pygame.Surface]:
        """
        Cut characters.png into one 32×32 Surface per direction.
        Returns a dict: {"up": Surface, "down_right": Surface, ...}
        """
        sheet  = pygame.image.load(str(char_sheet)).convert_alpha()
        frames = {}
        for direction, (row, col) in DIRECTION_COORDS.items():
            # Create a blank surface the size of one sprite cell
            frame = pygame.Surface((SPRITE_W, SPRITE_H))
            # Copy the correct cell out of the big spritesheet
            # blit(source, dest_pos, source_rect)
            frame.blit(sheet, (0, 0), pygame.Rect(COL_X[col], ROW_Y[row], SPRITE_W, SPRITE_H))
            # Mark the cyan color as transparent (colorkey = "treat this color as alpha=0")
            frame.set_colorkey(COLORKEY)
            frames[direction] = frame
        return frames