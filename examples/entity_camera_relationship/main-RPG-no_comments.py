import sys
import pygame
from pathlib import Path


# ── Resolve asset paths regardless of where you run the script from ─────────
#
# This file lives at: M151_Engine/example/entity_camera_relationship/main.py
#   Path(__file__).resolve()      → absolute path to this file
#   .parent                       → entity_camera_relationship/
#   .parent.parent                → example/
#   .parent.parent.parent         → M151_Engine/  ← project root
#
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
CHAR_SHEET   = PROJECT_ROOT / "assets" / "images" / "characters" / "characters.png"
MAP_IMAGE    = PROJECT_ROOT / "assets" / "images" / "background" / "land" / "test-land.png"


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

# Maps each direction string to its (sheet_row, sheet_col) in characters.png
_DIR_COORDS = {
    "up_left":    (0, 0),
    "up":         (0, 1),
    "up_right":   (0, 2),
    "right":      (0, 3),
    "left":       (1, 0),
    "down_left":  (1, 1),
    "down":       (1, 2),
    "down_right": (1, 3),
}


# ════════════════════════════════════════════════════════════════════════════
# HELPER: spritesheet loader
# ════════════════════════════════════════════════════════════════════════════

def load_frames() -> dict[str, pygame.Surface]:
    """
    Cut characters.png into one 32×32 Surface per direction.
    Returns a dict: {"up": Surface, "down_right": Surface, ...}
    """
    sheet  = pygame.image.load(str(CHAR_SHEET)).convert_alpha()
    frames = {}
    for direction, (row, col) in _DIR_COORDS.items():
        # Create a blank surface the size of one sprite cell
        frame = pygame.Surface((SPRITE_W, SPRITE_H))
        # Copy the correct cell out of the big spritesheet
        # blit(source, dest_pos, source_rect)
        frame.blit(sheet, (0, 0), pygame.Rect(_COL_X[col], _ROW_Y[row], SPRITE_W, SPRITE_H))
        # Mark the cyan color as transparent (colorkey = "treat this color as alpha=0")
        frame.set_colorkey(_COLORKEY)
        frames[direction] = frame
    return frames


# ════════════════════════════════════════════════════════════════════════════
# HELPER: keyboard input
# ════════════════════════════════════════════════════════════════════════════

def read_keys() -> tuple[float, float, str | None]:
    DIAG = 0.707   # 1 / √2

    keys = pygame.key.get_pressed()
    w = keys[pygame.K_w]
    s = keys[pygame.K_s]
    a = keys[pygame.K_a]
    d = keys[pygame.K_d]

    # Python's match statement on a tuple of booleans is a clean way to
    # handle 8-directional logic without a chain of if/elif.
    # Opposing keys (W+S or A+D) fall through to the default: no movement.
    match (w, s, a, d):
        case (True,  False, True,  False): return (-DIAG, -DIAG, "up_left")
        case (True,  False, False, True):  return ( DIAG, -DIAG, "up_right")
        case (False, True,  True,  False): return (-DIAG,  DIAG, "down_left")
        case (False, True,  False, True):  return ( DIAG,  DIAG, "down_right")
        case (True,  False, False, False): return ( 0.0,  -1.0,  "up")
        case (False, True,  False, False): return ( 0.0,   1.0,  "down")
        case (False, False, True,  False): return (-1.0,   0.0,  "left")
        case (False, False, False, True):  return ( 1.0,   0.0,  "right")
        case _:                            return ( 0.0,   0.0,  None)


# ════════════════════════════════════════════════════════════════════════════
# ENTITY
# ════════════════════════════════════════════════════════════════════════════

class Entity:
    SPEED = 220   # pixels per second in world space

    def __init__(self, world_x: float, world_y: float, frames: dict):
        self.world_x   = float(world_x)
        self.world_y   = float(world_y)
        self.direction = "down"   # facing direction, used to pick the sprite frame
        self.frames    = frames

        # Scale up for visibility: 32×32 px is tiny on a modern screen
        self.scale  = 1
        self.draw_w = SPRITE_W * self.scale   # 128 px
        self.draw_h = SPRITE_H * self.scale   # 128 px

    def update(self, dt: float, map_w: int, map_h: int) -> None:      
        dx, dy, new_dir = read_keys()

        if new_dir is not None:
            self.direction = new_dir

        self.world_x += dx * self.SPEED * dt
        self.world_y += dy * self.SPEED * dt

        # Clamp: keep the sprite fully inside the map
        self.world_x = max(0.0, min(self.world_x, map_w - self.draw_w))
        self.world_y = max(0.0, min(self.world_y, map_h - self.draw_h))

    def draw(self, screen: pygame.Surface, screen_x: float, screen_y: float) -> None:
        sprite = self.frames[self.direction]
        scaled = pygame.transform.scale(sprite, (self.draw_w, self.draw_h))
        screen.blit(scaled, (int(screen_x), int(screen_y)))


# ════════════════════════════════════════════════════════════════════════════
# CAMERA
# ════════════════════════════════════════════════════════════════════════════

class Camera:  
    def __init__(self, screen_w: int, screen_h: int):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.x = 0.0   # world x of the camera's left edge
        self.y = 0.0   # world y of the camera's top edge

    def follow(self, entity: Entity, map_w: int, map_h: int) -> None:
        # Entity's visual center in world space
        center_x = entity.world_x + entity.draw_w / 2
        center_y = entity.world_y + entity.draw_h / 2

        # Ideal camera top-left to center on that point
        target_x = center_x - self.screen_w / 2
        target_y = center_y - self.screen_h / 2

        # Clamp: don't scroll past map edges
        self.x = max(0.0, min(target_x, float(map_w - self.screen_w)))
        self.y = max(0.0, min(target_y, float(map_h - self.screen_h)))

    def world_to_screen(self, world_x: float, world_y: float) -> tuple[float, float]:
        return world_x - self.x, world_y - self.y

    def draw_map(self, screen: pygame.Surface, map_surface: pygame.Surface) -> None:
        screen.blit(
            map_surface,
            (0, 0),
            area=(int(self.x), int(self.y), self.screen_w, self.screen_h),
        )


# ════════════════════════════════════════════════════════════════════════════
# DEBUG OVERLAY
# ════════════════════════════════════════════════════════════════════════════

def draw_debug(
    screen: pygame.Surface,
    font: pygame.font.Font,
    player: Entity,
    camera: Camera,
) -> None:
    sx, sy = camera.world_to_screen(player.world_x, player.world_y)

    lines = [
        f"  world  : ({player.world_x:7.1f}, {player.world_y:7.1f})",
        f"  camera : ({camera.x:7.1f}, {camera.y:7.1f})",
        f"  screen : ({sx:7.1f}, {sy:7.1f})  = world - camera",
    ]

    panel_w = 340
    panel_h = len(lines) * 18 + 12
    panel   = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
    panel.fill((0, 0, 0, 160))   # semi-transparent black
    screen.blit(panel, (6, 6))

    for i, line in enumerate(lines):
        text = font.render(line, True, (180, 255, 160))
        screen.blit(text, (8, 10 + i * 18))


# ════════════════════════════════════════════════════════════════════════════
# ENTRY POINT
# ════════════════════════════════════════════════════════════════════════════

def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption("Entity–Camera Relationship — M151 Engine Example")
    clock = pygame.time.Clock()
    font  = pygame.font.SysFont("monospace", 14)

    # Load assets
    map_surface      = pygame.image.load(str(MAP_IMAGE)).convert()
    map_w, map_h     = map_surface.get_size()
    frames           = load_frames()

    # Spawn the player near the center of the world map
    player = Entity(world_x=map_w / 2, world_y=map_h / 2, frames=frames)

    camera = Camera(SCREEN_W, SCREEN_H)

    running = True
    while running:
        # ── Time ────────────────────────────────────────────────────────────
        # clock.tick(60) sleeps until 1/60th of a second has passed since
        # the last call, then returns the actual milliseconds elapsed.
        # Dividing by 1000 gives dt in seconds, which scales movement correctly.
        dt = clock.tick(60) / 1000.0

        # ── Events ──────────────────────────────────────────────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        # ── Update ──────────────────────────────────────────────────────────

        # 1. Move the entity in world space.
        player.update(dt, map_w, map_h)

        # 2. Update the camera AFTER the entity moves.
        #    This ensures the camera tracks the entity's NEW position.
        #    (If you swapped these, the camera would always be one frame behind.)
        camera.follow(player, map_w, map_h)

        # ── Draw ────────────────────────────────────────────────────────────
        # Drawing order matters: map first, then entities on top.

        # 3. Draw the visible slice of the world map.
        camera.draw_map(screen, map_surface)

        # 4. Convert the entity's world position to screen position, then draw.
        #    This single line IS the entity–camera relationship in practice:
        #        subtract camera → get screen coordinates → draw there.
        screen_x, screen_y = camera.world_to_screen(player.world_x, player.world_y)
        player.draw(screen, screen_x, screen_y)

        # 5. Debug overlay (drawn last so it appears on top of everything)
        draw_debug(screen, font, player, camera)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
