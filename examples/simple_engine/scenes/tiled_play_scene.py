"""
TiledPlayScene -- the exact same gameplay as PlayScene, but the map and
enemy spawns come from a Tiled-authored level (data/level1.tmj) instead
of config.MAP_IMAGE + data/enemies.json.

Nothing in engine/, Player, Enemy, or Missile changes to make this work.
Only WHERE the spawn data comes from is different -- proof that
EntityManager and CollisionSystem never cared how an entity's starting
position was decided. Compare this file's __init__ against
PlayScene.__init__ in play_scene.py: everything after "build the
entities" is identical.
"""
import pygame

from engine import config
from engine.scene import Scene
from engine.resource_loader import ResourceLoader
from engine.entity_manager import EntityManager
from engine.camera import Camera
from engine.tilemap import TiledMap
from engine import collision

from entities.player import Player
from entities.enemy import Enemy
from entities.missile import Missile

LEVEL_TMJ = config.DATA_DIR / "level1.tmj"


class TiledPlayScene(Scene):
    def __init__(self):
        self.resources = ResourceLoader()
        self.entities  = EntityManager()
        self.show_hitboxes = False
        self._next_entity_id = 1

        tiled_map = TiledMap(LEVEL_TMJ)

        background = tiled_map.image_layer("background")
        self.map_surface       = self.resources.load_image(background["path"])
        self.map_w, self.map_h = self.map_surface.get_size()

        player_frames = self.resources.load_directional_frames(
            config.CHAR_SHEET, config.PLAYER_SHEET_COORDS, config.PLAYER_SCALE)
        self._enemy_frames = self.resources.load_directional_frames(
            config.CHAR_SHEET, config.ENEMY_SHEET_COORDS, config.ENEMY_SCALE)
        self._missile_frames = self.resources.load_directional_frames(
            config.CHAR_SHEET, config.MISSILE_SHEET_COORDS, config.MISSILE_SCALE)

        self.player = self.entities.add(
            Player(self._new_id(), self.map_w / 2, self.map_h / 2, player_frames),
            group="player",
        )
        self.camera = Camera(config.SCREEN_W, config.SCREEN_H, self.player)

        # Tiled objects already store absolute world-pixel coordinates --
        # unlike data/enemies.json's offset-from-center convention, there's
        # no map_w/2 math here. The point object's (x, y) IS the spawn point.
        for spec in tiled_map.object_layer("enemies"):
            enemy = Enemy(
                spec["name"] or self._new_id(),
                spec["x"], spec["y"],
                self._enemy_frames,
                trail=spec["properties"].get("trail", "patrol"),
                speed=spec["properties"].get("speed", config.ENEMY_SPEED),
            )
            self.entities.add(enemy, group="enemies")

        self.font = pygame.font.SysFont("monospace", 16)

    def _new_id(self):
        entity_id, self._next_entity_id = self._next_entity_id, self._next_entity_id + 1
        return entity_id

    def handle_event(self, event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
            elif event.key == pygame.K_SPACE:
                self._fire_missile()
            elif event.key == pygame.K_F1:
                self.show_hitboxes = not self.show_hitboxes

    def _fire_missile(self) -> None:
        center_x, center_y = self.player.center()
        half_size = (config.SPRITE_W * config.MISSILE_SCALE) / 2
        missile = Missile(
            self._new_id(),
            center_x - half_size, center_y - half_size,
            self.player.direction,
            self._missile_frames[self.player.direction],
        )
        self.entities.add(missile, group="missiles")

    def update(self, dt: float) -> None:
        self.entities.update(dt, self.map_w, self.map_h)
        self.camera.follow(self.player, self.map_w, self.map_h)
        collision.check_groups(
            self.entities.group("missiles"),
            self.entities.group("enemies"),
            on_hit=self._on_missile_hit_enemy,
        )
        self.entities.purge_dead()

    def _on_missile_hit_enemy(self, missile, enemy) -> None:
        missile.kill()
        enemy.kill()
        print(f"Enemy '{enemy.id}' destroyed!")

    def draw(self, surface: pygame.Surface) -> None:
        self.camera.draw_map(surface, self.map_surface)
        self.entities.draw(surface, self.camera, draw_order=["enemies", "player", "missiles"])

        if self.show_hitboxes:
            for group in ("enemies", "player", "missiles"):
                collision.draw_debug_hitboxes(surface, self.camera, self.entities.group(group))

        self._draw_hud(surface)

    def _draw_hud(self, surface: pygame.Surface) -> None:
        lines = [
            "[Tiled-loaded level]  WASD move   SPACE shoot   F1 hitboxes "
            f"({'on' if self.show_hitboxes else 'off'})   ESC quit",
            f"enemies remaining: {self.entities.count('enemies')}",
        ]
        for i, line in enumerate(lines):
            text = self.font.render(line, True, (255, 255, 255))
            surface.blit(text, (8, 8 + i * 18))
