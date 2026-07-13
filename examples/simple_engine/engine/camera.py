"""
Camera -- a rectangular window into the world.

self.x / self.y are the WORLD coordinates of the camera's top-left
corner. Everything the camera "sees" is the map slice from (x, y) to
(x + screen_w, y + screen_h). See "Chapter 2 -- Camera & Coordinate
Spaces" in the PDF guide for the full worked-example derivation of
follow() and world_to_screen().
"""
import pygame


class Camera:
    def __init__(self, screen_w: int, screen_h: int, target):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.x = target.world_x - screen_w / 2
        self.y = target.world_y - screen_h / 2

    def follow(self, target, map_w: int, map_h: int) -> None:
        """
        Keep `target` roughly centered, with a dead-zone so the camera
        doesn't jitter on every tiny movement, then clamp to map edges so
        we never scroll past the edge of the world.
        """
        center_x = target.world_x + target.draw_w / 2
        center_y = target.world_y + target.draw_h / 2

        target_x, target_y = self.x, self.y

        # Dead-zone: only re-aim once the target drifts past the middle
        # third of the screen horizontally, or half/four-fifths vertically.
        if (center_x - target_x) <= self.screen_w / 3:
            target_x = center_x - self.screen_w / 3
        elif (center_x - target_x) >= self.screen_w / 3 * 2:
            target_x = center_x - self.screen_w / 3 * 2

        if (center_y - target_y) <= self.screen_h / 2:
            target_y = center_y - self.screen_h / 2
        elif (center_y - target_y) >= self.screen_h / 5 * 4:
            target_y = center_y - self.screen_h / 5 * 4

        self.x = max(0.0, min(target_x, float(map_w - self.screen_w)))
        self.y = max(0.0, min(target_y, float(map_h - self.screen_h)))

    def world_to_screen(self, world_x: float, world_y: float) -> tuple[float, float]:
        """screen = world - camera. Works for ANY world-space point."""
        return world_x - self.x, world_y - self.y

    def draw_map(self, surface: pygame.Surface, map_surface: pygame.Surface) -> None:
        """
        Blit only the visible slice of the map using area=, so the cost
        stays constant (screen_w x screen_h pixels) no matter how large
        the map image actually is.
        """
        surface.blit(
            map_surface,
            (0, 0),
            area=(int(self.x), int(self.y), self.screen_w, self.screen_h),
        )
