import pygame
import sys

'''
  ┌──────────────┬──────────────────────────────────────────────────────────┐                                                                                                                                                                                                                                                 
  │    Thing     │                          Detail                          │                                                                                                                                                                                                                                               
  ├──────────────┼──────────────────────────────────────────────────────────┤                                                                                                                                                                                                                                                 
  │ Screen       │ 960×540 window (a nice 16:9 view into the 4113×1598 map) │                                                                                                                                                                                                                                               
  ├──────────────┼──────────────────────────────────────────────────────────┤
  │ Scrolling    │ WASD keys, frame-rate independent via dt (delta-time)    │                                                                                                                                                                                                                                                 
  ├──────────────┼──────────────────────────────────────────────────────────┤                                                                                                                                                                                                                                                 
  │ Speed        │ 300 px/sec — change SCROLL_SPEED at the top              │                                                                                                                                                                                                                                                 
  ├──────────────┼──────────────────────────────────────────────────────────┤                                                                                                                                                                                                                                                 
  │ Camera clamp │ Prevents scrolling past map edges in any direction       │                                                                                                                                                                                                                                               
  ├──────────────┼──────────────────────────────────────────────────────────┤                                                                                                                                                                                                                                                 
  │ Exit         │ Esc or closing the window                                │                                                                                                                                                                                                                                               
  └──────────────┴──────────────────────────────────────────────────────────┘            
'''
# --- Config ---
SCREEN_W, SCREEN_H = 960, 540
SCROLL_SPEED = 300          # pixels per second
MAP_PATH = "assets/background/land/test-land.png"

def display_map():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption("Map Scroll Test — WASD to scroll")
    clock = pygame.time.Clock()

    land_map = pygame.image.load(MAP_PATH).convert_alpha()
    map_w, map_h = land_map.get_size()

    # Camera offset — top-left corner of the view into the map
    cam_x, cam_y = 0.0, 0.0

    while True:
        dt = clock.tick(60) / 1000.0   # seconds since last frame

        # --- Events ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

        # --- Input ---
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            cam_x -= SCROLL_SPEED * dt
        if keys[pygame.K_d]:
            cam_x += SCROLL_SPEED * dt
        if keys[pygame.K_w]:
            cam_y -= SCROLL_SPEED * dt
        if keys[pygame.K_s]:
            cam_y += SCROLL_SPEED * dt

        # Clamp camera so it never goes outside the map
        cam_x = max(0, min(cam_x, map_w - SCREEN_W))
        cam_y = max(0, min(cam_y, map_h - SCREEN_H))

        # --- Draw ---
        screen.blit(land_map, (0, 0), area=(int(cam_x), int(cam_y), SCREEN_W, SCREEN_H))

        pygame.display.flip()

if __name__ == "__main__":
    main()
