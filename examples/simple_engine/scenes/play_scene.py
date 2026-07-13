"""
PlayScene -- wires every engine system together into one playable demo:
WASD to move, SPACE to shoot, hit an enemy with a missile to destroy it.

This is the piece that replaces main.py / main-with_enemy.py /
main-with_spawner.py from the main M151_Engine prototypes. Instead of
three separate copy-pasted game loops, there is ONE Scene -- and adding a
menu or a game-over screen later just means writing another Scene and
pointing Game at it (see engine/scene.py).
"""
import pygame

from engine import config
from engine.scene import Scene
from engine.resource_loader import ResourceLoader
from engine.entity_manager import EntityManager
from engine.camera import Camera
from engine.spawner import JSONSpawner
from engine import collision

from entities.player import Player
from entities.enemy import Enemy
from entities.missile import Missile


class PlayScene(Scene):
    def __init__(self):
        self.resources = ResourceLoader()
        self.entities  = EntityManager()
        self.show_hitboxes = False
        self._next_entity_id = 1

        self.map_surface        = self.resources.load_image(config.MAP_IMAGE)
        self.map_w, self.map_h  = self.map_surface.get_size()

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

        spawner = JSONSpawner(config.ENEMIES_JSON, self.map_w, self.map_h)
        for enemy in spawner.load("enemies", self._make_enemy):
            self.entities.add(enemy, group="enemies")

        self.font = pygame.font.SysFont("monospace", 16)

    def _new_id(self):
        entity_id, self._next_entity_id = self._next_entity_id, self._next_entity_id + 1
        return entity_id

    def _make_enemy(self, spec: dict, world_x: float, world_y: float) -> Enemy:
        """Factory handed to JSONSpawner -- see engine/spawner.py."""
        return Enemy(
            spec.get("id", self._new_id()),
            world_x, world_y,
            self._enemy_frames,
            trail=spec.get("trail", "patrol"),
            speed=spec.get("speed", config.ENEMY_SPEED),
        )

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
        # 1. Move everything in world space.
        self.entities.update(dt, self.map_w, self.map_h)

        # 2. Camera tracks the player's NEW position -- always update the
        #    camera AFTER entities move, or it lags one frame behind.
        self.camera.follow(self.player, self.map_w, self.map_h)

        # 3. Resolve collisions, then sweep out anything killed this frame.
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
        # Drawing order matters: map first, then entities on top of it.
        self.camera.draw_map(surface, self.map_surface)
        self.entities.draw(surface, self.camera, draw_order=["enemies", "player", "missiles"])

        if self.show_hitboxes:
            for group in ("enemies", "player", "missiles"):
                collision.draw_debug_hitboxes(surface, self.camera, self.entities.group(group))

        self._draw_hud(surface)

    def _draw_hud(self, surface: pygame.Surface) -> None:
        lines = [
            f"WASD move   SPACE shoot   F1 hitboxes ({'on' if self.show_hitboxes else 'off'})   ESC quit",
            f"enemies remaining: {self.entities.count('enemies')}",
        ]
        for i, line in enumerate(lines):
            text = self.font.render(line, True, (255, 255, 255))
            surface.blit(text, (8, 8 + i * 18))
