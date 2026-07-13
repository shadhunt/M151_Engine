"""
CollisionSystem -- rectangle overlap checks between entity groups.

Kept deliberately simple: pygame.Rect.collidelist() is O(n) per query,
which is completely fine at the entity counts a learning project deals
with (tens of entities, not thousands). A spatial grid or quadtree only
starts to matter once you have hundreds of moving colliders on screen at
once -- a real future upgrade, not something to build before you need it.
"""
import pygame


def check_groups(group_a: list, group_b: list, on_hit) -> None:
    """
    Compare every entity in group_a against every entity in group_b using
    world-space hitboxes. Calls on_hit(entity_a, entity_b) for each
    overlapping pair found this frame.
    """
    if not group_a or not group_b:
        return

    b_boxes = [b.get_hitbox() for b in group_b]
    for a in group_a:
        if not a.alive:
            continue
        hit_index = a.get_hitbox().collidelist(b_boxes)
        if hit_index != -1:
            on_hit(a, group_b[hit_index])


def draw_debug_hitboxes(surface: pygame.Surface, camera, entities: list, color=(255, 0, 255)) -> None:
    """Outline every entity's hitbox in screen space. PlayScene toggles this with F1."""
    for entity in entities:
        if not entity.alive:
            continue
        world_rect = entity.get_hitbox()
        screen_x, screen_y = camera.world_to_screen(world_rect.x, world_rect.y)
        screen_rect = pygame.Rect(int(screen_x), int(screen_y), world_rect.w, world_rect.h)
        pygame.draw.rect(surface, color, screen_rect, 2)
