"""
Entity -- the one shape every game object conforms to.

In the main M151_Engine prototypes, Player and Enemy inherited from
Entity but Missile did not, even though it had the exact same
world_x/world_y/update/draw shape. That inconsistency is why every
prototype had to hand-write its own missile-vs-enemy collision check
instead of a generic "check group A against group B". Here everything
that lives in the world -- player, enemies, missiles, future pickups --
inherits from Entity, so EntityManager and CollisionSystem can treat
them all the same way.
"""
import pygame


class Entity:
    def __init__(self, entity_id, world_x: float, world_y: float, draw_w: int, draw_h: int):
        self.id      = entity_id
        self.world_x = float(world_x)
        self.world_y = float(world_y)
        self.draw_w  = draw_w
        self.draw_h  = draw_h
        self.alive   = True   # EntityManager.purge_dead() sweeps these out after update()

    def kill(self) -> None:
        """
        Mark for removal. Actual removal happens later, in
        EntityManager.purge_dead() -- never mid-iteration. Removing an
        item from a list while looping over that same list skips the
        element right after the one you removed, a classic source of
        "the hit enemy didn't actually disappear" bugs.
        """
        self.alive = False

    def update(self, dt: float, map_w: int, map_h: int) -> None:
        raise NotImplementedError

    def draw(self, surface: pygame.Surface, camera) -> None:
        raise NotImplementedError

    def get_hitbox(self) -> pygame.Rect:
        """
        Hitbox in WORLD space. Collision is always computed in world
        space, never screen space, so it stays correct no matter where
        the camera is currently looking.
        """
        return pygame.Rect(int(self.world_x), int(self.world_y), self.draw_w, self.draw_h)
