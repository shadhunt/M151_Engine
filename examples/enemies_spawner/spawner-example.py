import pygame
import sys
import json
from pathlib import Path

FRAMEWORK_ROOT = str(Path(__file__).resolve().parents[2])
sys.path.append(FRAMEWORK_ROOT)

from config.properties import *
from config.path_config import *
from config.analog_control_const import *
from core.entities.entity import Entity
from core.entities.missile import Missile
from core.camera.camera import Camera
from gameplay.graphics.graphic_loader import GraphicLoader

# ── Skin registry ─────────────────────────────────────────────────────────────
#
# Maps the "skin" string in enemies.json to the direction-coord dict that
# GraphicLoader.load_frames() needs to cut sprites from characters.png.
# To add a new skin, add its row/col coords to analog_control_const.py
# (like ENEMY_DIRECTION_COORDS) and register it here.
#
SKIN_REGISTRY = {
    "gray_vehicle": ENEMY_DIRECTION_COORDS,
}


# ── ConfigEnemy ───────────────────────────────────────────────────────────────

class ConfigEnemy:
    """
    An enemy whose position, skin, speed, and movement style come from
    a JSON config entry instead of being hardcoded.

    Three trail styles
    ------------------
    "patrol"
        Cycles through all 8 compass directions (ENEMY_PATH) on a fixed
        timer.  The enemy smoothly loops around — same behaviour as the
        enemy in main-with_enemy.py.

    "bounce"
        Moves diagonally like a billiard ball.  When the enemy hits a
        left/right wall it flips its horizontal velocity; top/bottom wall
        flips the vertical velocity.  Direction facing updates to match.

    "zigzag"
        Alternates between a horizontal run and a vertical run, switching
        every 1.5 seconds.  Produces an L-shaped path.  Reverses along
        whichever axis it hits a wall on.
    """

    def __init__(self, world_x, world_y, frames, trail="patrol", speed=ENEMY_SPEED):
        self.world_x  = float(world_x)
        self.world_y  = float(world_y)
        self.trail    = trail
        self.speed    = speed

        self.scale  = ENEMY_SCALE
        self.draw_w = SPRITE_W * self.scale
        self.draw_h = SPRITE_H * self.scale

        self._scaled_frames = {
            d: pygame.transform.scale(f, (self.draw_w, self.draw_h))
            for d, f in frames.items()
        }

        # ── patrol state ──────────────────────────────────────────────────────
        # Start at index 0 of ENEMY_PATH and rotate forward each tick.
        self._patrol_index  = 0
        self._patrol_timer  = 0.0
        self._patrol_every  = 0.85          # seconds between direction changes

        self.direction = ENEMY_PATH[self._patrol_index]
        self.image     = self._scaled_frames[self.direction]

        # ── bounce state ──────────────────────────────────────────────────────
        # _bvx / _bvy are sign values (+1 or -1) for the diagonal velocity.
        # We multiply them by self.speed each frame, so they represent direction
        # only — not magnitude.  Flipping a sign reverses that axis.
        self._bvx = 1.0
        self._bvy = 1.0

        # ── zigzag state ──────────────────────────────────────────────────────
        # _zz_phase 0 → moving along X axis
        # _zz_phase 1 → moving along Y axis
        # _zz_sign  → +1 (positive direction) or -1 (negative direction)
        self._zz_phase       = 0
        self._zz_timer       = 0.0
        self._zz_switch_every = 1.5         # seconds per phase
        self._zz_sign        = 1.0

    # ── public API ────────────────────────────────────────────────────────────

    def update(self, dt, map_w, map_h):
        if self.trail == "patrol":
            self._update_patrol(dt, map_w, map_h)
        elif self.trail == "bounce":
            self._update_bounce(dt, map_w, map_h)
        elif self.trail == "zigzag":
            self._update_zigzag(dt, map_w, map_h)

    def draw(self, surface, screen_x, screen_y):
        surface.blit(self.image, (int(screen_x), int(screen_y)))

    def get_hitbox(self, screen_x, screen_y):
        # Hitbox is the enemy's bounding rectangle in world space.
        return pygame.Rect(self.world_x, self.world_y, self.draw_w, self.draw_h)

    # ── trail implementations ─────────────────────────────────────────────────

    def _update_patrol(self, dt, map_w, map_h):
        """Rotate through all 8 directions on a fixed timer."""
        self._patrol_timer += dt
        if self._patrol_timer >= self._patrol_every:
            self._patrol_timer = 0.0
            self._patrol_index = (self._patrol_index + 1) % len(ENEMY_PATH)
            self.direction     = ENEMY_PATH[self._patrol_index]
            self.image         = self._scaled_frames[self.direction]

        vx, vy = self._direction_vector(self.direction)
        self.world_x += vx * self.speed * dt
        self.world_y += vy * self.speed * dt
        self._clamp(map_w, map_h)

    def _update_bounce(self, dt, map_w, map_h):
        """Billiard-ball diagonal bounce off the map walls."""
        self.world_x += self._bvx * self.speed * dt
        self.world_y += self._bvy * self.speed * dt

        # Flip the horizontal component and snap to the wall
        if self.world_x <= 0:
            self.world_x = 0.0
            self._bvx = 1.0
        elif self.world_x >= map_w - self.draw_w:
            self.world_x = float(map_w - self.draw_w)
            self._bvx = -1.0

        # Flip the vertical component and snap to the wall
        if self.world_y <= 0:
            self.world_y = 0.0
            self._bvy = 1.0
        elif self.world_y >= map_h - self.draw_h:
            self.world_y = float(map_h - self.draw_h)
            self._bvy = -1.0

        # Update the sprite frame to match the current travel direction
        self.direction = self._direction_from_signs(self._bvx, self._bvy)
        self.image     = self._scaled_frames[self.direction]

    def _update_zigzag(self, dt, map_w, map_h):
        """Alternate between horizontal and vertical movement every N seconds."""
        self._zz_timer += dt
        if self._zz_timer >= self._zz_switch_every:
            self._zz_timer = 0.0
            self._zz_phase = 1 - self._zz_phase   # flip between 0 and 1

        if self._zz_phase == 0:
            # Horizontal leg
            self.world_x += self._zz_sign * self.speed * dt
            if self.world_x <= 0 or self.world_x >= map_w - self.draw_w:
                self._zz_sign *= -1               # reverse on wall hit
            self.direction = RIGHT if self._zz_sign > 0 else LEFT
        else:
            # Vertical leg
            self.world_y += self._zz_sign * self.speed * dt
            if self.world_y <= 0 or self.world_y >= map_h - self.draw_h:
                self._zz_sign *= -1
            self.direction = DOWN if self._zz_sign > 0 else UP

        self._clamp(map_w, map_h)
        self.image = self._scaled_frames[self.direction]

    # ── helpers ───────────────────────────────────────────────────────────────

    def _direction_vector(self, direction):
        return {
            UP:         ( 0.0,    -1.0),
            DOWN:       ( 0.0,     1.0),
            LEFT:       (-1.0,     0.0),
            RIGHT:      ( 1.0,     0.0),
            UP_LEFT:    (-0.707,  -0.707),
            UP_RIGHT:   ( 0.707,  -0.707),
            DOWN_LEFT:  (-0.707,   0.707),
            DOWN_RIGHT: ( 0.707,   0.707),
        }.get(direction, (0.0, 0.0))

    def _direction_from_signs(self, vx, vy):
        # Map the sign of each velocity component to the matching direction string.
        if vx > 0 and vy < 0: return UP_RIGHT
        if vx < 0 and vy < 0: return UP_LEFT
        if vx > 0 and vy > 0: return DOWN_RIGHT
        if vx < 0 and vy > 0: return DOWN_LEFT
        if vx > 0:             return RIGHT
        if vx < 0:             return LEFT
        if vy > 0:             return DOWN
        return UP

    def _clamp(self, map_w, map_h):
        self.world_x = max(0.0, min(self.world_x, map_w - self.draw_w))
        self.world_y = max(0.0, min(self.world_y, map_h - self.draw_h))

    def __del__(self):
        print(f"Enemy '{getattr(self, 'id', '?')}' destroyed")


# ── EnemySpawner ──────────────────────────────────────────────────────────────

class EnemySpawner:
    """
    Reads enemies.json and returns a ready-to-use list of ConfigEnemy objects.

    JSON fields per enemy
    ---------------------
    id                    : label printed when the enemy is hit or destroyed
    spawn_x_from_center   : pixel offset from the horizontal centre of the map
    spawn_y_from_center   : pixel offset from the vertical centre of the map
    skin                  : key into SKIN_REGISTRY (e.g. "gray_vehicle")
    trail                 : movement style — "patrol", "bounce", or "zigzag"
    speed                 : pixels per second

    Using offsets from the map centre (rather than absolute pixels) means the
    config works with any map size — the spawner adds map_w/2 + offset to get
    the final world position.
    """

    def __init__(self, json_path, graphic_loader, map_w, map_h):
        self._json_path      = Path(json_path)
        self._graphic_loader = graphic_loader
        self._map_w          = map_w
        self._map_h          = map_h

    def load(self):
        with open(self._json_path) as f:
            data = json.load(f)

        enemies = []
        for cfg in data["enemies"]:
            skin_coords = SKIN_REGISTRY.get(cfg["skin"], ENEMY_DIRECTION_COORDS)
            frames      = self._graphic_loader.load_frames(skin_coords)

            world_x = self._map_w / 2 + cfg.get("spawn_x_from_center", 0)
            world_y = self._map_h / 2 + cfg.get("spawn_y_from_center", 0)

            enemy    = ConfigEnemy(
                world_x = world_x,
                world_y = world_y,
                frames  = frames,
                trail   = cfg.get("trail", "patrol"),
                speed   = cfg.get("speed", ENEMY_SPEED),
            )
            enemy.id = cfg.get("id", "unknown")
            enemies.append(enemy)

        print(f"Spawned {len(enemies)} enemies from {self._json_path.name}")
        return enemies


# ── Main ──────────────────────────────────────────────────────────────────────

class Main:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Enemy Spawner Example")
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        self.clock  = pygame.time.Clock()

        self.map_surface       = pygame.image.load(str(MAP_IMAGE)).convert()
        self.map_w, self.map_h = self.map_surface.get_size()

        graphic_loader = GraphicLoader(CHAR_SHEET)

        player_frames        = graphic_loader.load_frames(PLAYER_DIRECTION_COORDS)
        self.missile_frames  = graphic_loader.load_frames(MISSILE_COORDS)

        self.player = Entity(world_x=self.map_w / 2, world_y=self.map_h / 2, frames=player_frames)
        self.camera = Camera(SCREEN_W, SCREEN_H, self.player)

        json_path     = Path(__file__).parent / "enemies.json"
        spawner       = EnemySpawner(json_path, graphic_loader, self.map_w, self.map_h)
        self.enemies  = spawner.load()

        self.missiles = []
        self.running  = True

    def game_loop(self):
        while self.running:
            dt = self.clock.tick(60) / 1000.0

            # ── Mouse → world coordinate helper ───────────────────────────────
            #
            # screen_to_world is the reverse of camera.world_to_screen():
            #   world_x = mouse_screen_x + camera.x
            #   world_y = mouse_screen_y + camera.y
            #
            # Then subtract the map centre to get the spawn_*_from_center
            # values you paste directly into enemies.json.
            #
            msx, msy   = pygame.mouse.get_pos()
            mwx        = msx + self.camera.x
            mwy        = msy + self.camera.y
            offset_x   = int(mwx - self.map_w / 2)
            offset_y   = int(mwy - self.map_h / 2)
            pygame.display.set_caption(
                f"world ({int(mwx)}, {int(mwy)})  "
                f"spawn_from_center ({offset_x:+d}, {offset_y:+d})  "
                f"[left-click to print]"
            )

            # ── Events ────────────────────────────────────────────────────────
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    print(
                        f'{{"spawn_x_from_center": {offset_x}, '
                        f'"spawn_y_from_center": {offset_y}}}'
                    )
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    if event.key == pygame.K_SPACE:
                        mx = self.player.world_x + self.player.draw_w / 2 - Missile.half_size
                        my = self.player.world_y + self.player.draw_h / 2 - Missile.half_size
                        self.missiles.append(
                            Missile(mx, my, self.player.direction, self.missile_frames)
                        )

            # ── Update ────────────────────────────────────────────────────────
            self.player.update(dt, self.map_w, self.map_h)
            for enemy in self.enemies:
                enemy.update(dt, self.map_w, self.map_h)
            self.camera.follow(self.player, self.map_w, self.map_h)

            # ── Draw map and player ───────────────────────────────────────────
            self.camera.draw_map(self.screen, self.map_surface)
            px, py = self.camera.world_to_screen(self.player.world_x, self.player.world_y)
            self.player.draw(self.screen, px, py)

            # ── Draw all enemies and collect their hitboxes ───────────────────
            # We build the hitbox list in the same loop as drawing so each
            # hitbox index stays in sync with self.enemies indices.
            enemy_hitboxes = []
            for enemy in self.enemies:
                ex, ey = self.camera.world_to_screen(enemy.world_x, enemy.world_y)
                enemy.draw(self.screen, ex, ey)
                enemy_hitboxes.append(enemy.get_hitbox(ex, ey))

            # ── Update missiles ───────────────────────────────────────────────
            for m in self.missiles:
                m.update(dt)
            self.missiles = [
                m for m in self.missiles
                if not m.is_outside_view(self.camera.x, self.camera.y, SCREEN_W, SCREEN_H)
            ]

            # ── Draw missiles + collision detection ───────────────────────────
            killed = set()
            for m in self.missiles:
                msx, msy = self.camera.world_to_screen(m.x, m.y)
                m.draw(self.screen, msx, msy)

                if enemy_hitboxes:
                    hit_idx = m.get_hitbox(self.screen, msx, msy).collidelist(enemy_hitboxes)
                    if hit_idx != -1:
                        print(f"Enemy '{self.enemies[hit_idx].id}' hit!")
                        killed.add(hit_idx)

            # Remove killed enemies in reverse index order so earlier indices
            # stay valid as we delete.
            for i in sorted(killed, reverse=True):
                self.enemies.pop(i)

            pygame.display.flip()


if __name__ == "__main__":
    main = Main()
    main.game_loop()
