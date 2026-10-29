"""
ResourceLoader -- the ONE place that touches the filesystem for images.

Before: GraphicLoader (in the main M151_Engine gameplay/graphics folder)
loaded and cut sprite sheets, but every prototype still repeated the
"load a fresh copy of this image" call by hand and there was no cache.
Now: load once, cache forever, and hand out already-cut, already-scaled
Surfaces to anyone who asks -- Player, Enemy, and Missile all go through
this one class.
"""
import pygame

from . import config


class ResourceLoader:
    def __init__(self):
        self._image_cache: dict[str, pygame.Surface] = {}

    def load_image(self, path, colorkey=None, convert_alpha: bool = False) -> pygame.Surface:
        key = str(path)
        if key not in self._image_cache:
            surface = pygame.image.load(key)
            surface = surface.convert_alpha() if convert_alpha else surface.convert()
            if colorkey is not None:
                surface.set_colorkey(colorkey)
            self._image_cache[key] = surface
        return self._image_cache[key]

    def cell_position(self, col: int, row: int) -> tuple[int, int]:
        """
        Pixel (x, y) of a sheet cell's top-left corner, given its
        0-indexed (col, row). See config.py for the sheet layout.
        """
        x = config.SHEET_COL_START_X + col * config.SHEET_CELL_PITCH
        y = config.SHEET_ROW_START_Y + row * config.SHEET_CELL_PITCH
        return x, y

    def slice_sheet(self, sheet: pygame.Surface, coord_map: dict) -> dict:
        """Cut {direction: (row, col)} out of `sheet` into {direction: Surface}."""
        frames = {}
        for direction, (row, col) in coord_map.items():
            x, y = self.cell_position(col, row)
            cell = pygame.Surface((config.SPRITE_W, config.SPRITE_H))
            cell.blit(sheet, (0, 0), pygame.Rect(x, y, config.SPRITE_W, config.SPRITE_H))
            cell.set_colorkey(config.COLORKEY)
            frames[direction] = cell
        return frames

    def load_directional_frames(self, sheet_path, coord_map: dict, scale: int) -> dict:
        """
        High-level convenience: load a sheet, slice it by coord_map, and
        scale every resulting frame up by `scale`. Returns {direction:
        Surface}, ready to hand straight to an Animator.
        """
        sheet  = self.load_image(sheet_path, convert_alpha=True)
        frames = self.slice_sheet(sheet, coord_map)
        size   = (config.SPRITE_W * scale, config.SPRITE_H * scale)
        return {direction: pygame.transform.scale(frame, size) for direction, frame in frames.items()}
