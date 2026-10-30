"""
EntityManager -- a single registry for every Entity in the game,
organized into named groups ("player", "enemies", "missiles", ...).

This is the piece that was MISSING from every earlier M151_Engine
prototype. Without it, main-with_enemy.py used self.enemy (one hardcoded
slot) and main-with_spawner.py used self.enemies (a bare list), and each
prototype re-wrote its own update/draw/cleanup loop by hand. With
EntityManager, a Scene gets ONE update loop and ONE draw loop that work
no matter how many groups or entities exist.
"""
import pygame


class EntityManager:
    def __init__(self):
        self._groups: dict[str, list] = {}

    def add(self, entity, group: str = "default"):
        """Register an entity under `group` and return it (handy for
        one-line `self.player = self.entities.add(Player(...), "player")`)."""
        self._groups.setdefault(group, []).append(entity)
        return entity

    def group(self, group: str) -> list:
        """The live list for one group -- e.g. for collision checks."""
        return self._groups.get(group, [])

    def update(self, dt: float, map_w: int, map_h: int) -> None:
        for entities in self._groups.values():
            for entity in entities:
                if entity.alive:
                    entity.update(dt, map_w, map_h)

    def draw(self, surface: pygame.Surface, camera, draw_order: list[str] | None = None) -> None:
        """
        draw_order controls layering (e.g. draw enemies before the player
        so the player renders on top). Groups not listed are drawn
        afterward, in whatever order they were first added.
        """
        order = draw_order or list(self._groups.keys())
        for group in order:
            for entity in self._groups.get(group, []):
                if entity.alive:
                    entity.draw(surface, camera)

    def purge_dead(self) -> None:
        """
        Remove every entity with alive == False. Runs ONCE per frame,
        after update() and after collision checks -- never during a loop
        over the group itself (see Entity.kill() for why).
        """
        for group, entities in self._groups.items():
            self._groups[group] = [e for e in entities if e.alive]

    def count(self, group: str | None = None) -> int:
        if group is not None:
            return len(self._groups.get(group, []))
        return sum(len(v) for v in self._groups.values())
