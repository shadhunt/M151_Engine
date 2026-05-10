import pygame
from engine.entities.entity import Entity 
class Camera:
    """
    The camera defines a rectangular window into the world.

    self.x, self.y  →  world coordinates of the camera's TOP-LEFT corner.
                       "How far into the world have we scrolled?"

    Visual diagram:

        World map  (4113 × 1598 px)
        ┌──────────────────────────────────────────────────┐
        │                                                  │
        │   (cam_x, cam_y)                                 │
        │   ┌────────────────────┐ ← Camera viewport       │
        │   │   (screen 960×540) │                         │
        │   │                   │                         │
        │   │     [entity]       │                         │
        │   │                   │                         │
        │   └────────────────────┘                         │
        │                                                  │
        └──────────────────────────────────────────────────┘

    Only what's inside the camera rect is visible on screen.
    Everything outside is simply not drawn.
    """

    def __init__(self, screen_w: int, screen_h: int, player:Entity):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.x = player.world_x-screen_w/2.5   # world x of the camera's left edge
        self.y = player.world_y-screen_h/2.5 * 2
           # world y of the camera's top edge    

    def follow(self, entity: Entity, map_w: int, map_h: int) -> None:
        """
        Update the camera position to keep the entity centered on screen,
        clamped so we never show outside the map.

        ── STEP 1: aim for the entity's center ──────────────────────────────

        We want the VISUAL CENTER of the entity sprite to sit at the center
        of the screen. The sprite's visual center in world space is:

            center_x = entity.world_x + entity.draw_w / 2
            center_y = entity.world_y + entity.draw_h / 2

        For the camera's top-left to place that center in the middle of
        the screen, the camera must be at:

            target_x = center_x - screen_w / 2
            target_y = center_y - screen_h / 2

        You can verify this: if camera is at target_x,
            screen position of center = center_x - target_x
                                      = center_x - (center_x - screen_w/2)
                                      = screen_w / 2  ✓  (exactly the middle)

        ── STEP 2: clamp to map boundaries ──────────────────────────────────

        The camera's top-left must stay inside:

            x ∈ [0,  map_w - screen_w]
            y ∈ [0,  map_h - screen_h]

        If x < 0:             camera shows left of the map  → black strip.
        If x > map_w-screen_w: camera shows right of the map → black strip.

        When the entity is near an edge, the camera "stops" at the clamp
        limit while the entity continues moving. The entity visually slides
        toward the edge of the screen — this is the expected, correct behavior.
        """
        # Entity's visual center in world space
        center_x = entity.world_x + entity.draw_w / 2
        center_y = entity.world_y + entity.draw_h / 2

        # Ideal camera top-left to center on that point

        #original always center
        #target_x = center_x - self.screen_w / 2
        target_x = self.x
        target_y = self.y

        if(center_x - target_x) <= self.screen_w / 3:
            target_x = center_x - self.screen_w / 3
        elif (center_x - target_x) >= self.screen_w / 3 * 2:
            target_x = center_x - self.screen_w / 3 * 2


        if(center_y - target_y) <= self.screen_h / 2:
            target_y = center_y - self.screen_h / 2
        elif(center_y - target_y) >= self.screen_h / 5 * 4:
            target_y = center_y - self.screen_h / 5 * 4
        # Clamp: don't scroll past map edges
        #self.x = max(0.0, min(target_x, float(map_w - self.screen_w)))
        self.x = max(0.0, min(target_x, float(map_w - self.screen_w)))
        self.y = max(0.0, min(target_y, float(map_h - self.screen_h)))

    def world_to_screen(self, world_x: float, world_y: float) -> tuple[float, float]:
        """
        Convert any world-space coordinate to a screen-space coordinate.

        FORMULA:
            screen_x = world_x - cam_x
            screen_y = world_y - cam_y

        INTUITION:
            cam_x represents how far the camera has scrolled to the right.
            Subtracting it from a world x-coordinate "un-scrolls" it —
            it gives you where that world point appears relative to the
            left edge of the screen.

            Worked example:
                Entity is at world (2100, 800).
                Camera top-left is at world (1632, 565).
                screen_x = 2100 - 1632 = 468
                screen_y = 800  - 565  = 235
                → sprite is drawn at pixel (468, 235) on the window.

        NOTE: This formula works for ANY world object — enemies, items,
        particles, UI elements anchored to world positions, etc.
        Always subtract the camera before drawing anything in world space.
        """
        return world_x - self.x, world_y - self.y

    def draw_map(self, screen: pygame.Surface, map_surface: pygame.Surface) -> None:
        """
        Draw only the visible slice of the map onto the screen.

        EFFICIENT APPROACH — use pygame's area= parameter:
            screen.blit(map_surface, dest=(0,0), area=(cam_x, cam_y, W, H))

            This tells pygame: "starting at pixel (cam_x, cam_y) in the
            source image, copy a W×H rectangle and place it at (0,0) on
            the destination surface."

            Only 960×540 pixels are copied per frame, regardless of how
            large the map is. Blitting the full 4113×1598 map every frame
            would be far slower and unnecessary.

        ALTERNATIVE (simpler to understand, but slower):
            screen.blit(map_surface, (-cam_x, -cam_y))

            This draws the entire map at an offset, which achieves the
            same visual result but sends millions of off-screen pixels
            through the renderer unnecessarily.
        """
        screen.blit(
            map_surface,
            (0, 0),
            area=(int(self.x), int(self.y), self.screen_w, self.screen_h),
        )

