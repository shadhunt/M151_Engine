import pygame
from config.analog_control_const import _DIRECTION_COORDS


# ── Display settings ─────────────────────────────────────────────────────────
SCREEN_W = 960
SCREEN_H = 540


# ── Spritesheet constants (see main_character_actions.py for full explanation)
#
# characters.png is a grid of 32×32 sprite cells separated by 1-pixel lines.
# Column x-positions start at x=10, then repeat every 33 pixels (32 + 1 sep).
# Row y-positions: row 0 starts at y=25, row 1 starts at y=58.
#
SPRITE_W  = 32
SPRITE_H  = 32
_COL_X    = [10 + col * 33 for col in range(4)]   # [10, 43, 76, 109]
_ROW_Y    = [25, 58]
_COLORKEY = (32, 200, 248)   # cyan background → transparent

class GraphicLoader():
    def load_frames(char_sheet:str) -> dict[str, pygame.Surface]:
        """
        Cut characters.png into one 32×32 Surface per direction.
        Returns a dict: {"up": Surface, "down_right": Surface, ...}
        """
        sheet  = pygame.image.load(str(char_sheet)).convert_alpha()
        frames = {}
        for direction, (row, col) in _DIRECTION_COORDS.items():
            # Create a blank surface the size of one sprite cell
            frame = pygame.Surface((SPRITE_W, SPRITE_H))
            # Copy the correct cell out of the big spritesheet
            # blit(source, dest_pos, source_rect)
            frame.blit(sheet, (0, 0), pygame.Rect(_COL_X[col], _ROW_Y[row], SPRITE_W, SPRITE_H))
            # Mark the cyan color as transparent (colorkey = "treat this color as alpha=0")
            frame.set_colorkey(_COLORKEY)
            frames[direction] = frame
        return frames