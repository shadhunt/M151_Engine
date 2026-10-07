import pygame
import json
from pathlib import Path

class Main:

    def __init__(self):
        pygame.init()
        SCREEN_WIDTH=960
        SCREEN_HEIGHT=640
        self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
        self.clock  = pygame.time.Clock()
        
        map_path = Path("assets/maps/test_map.tmj")
        self.map_dir = map_path.parent

        with open(map_path, "r") as file:
            self.map_data = json.load(file)

        self.tile_width = self.map_data["tilewidth"]
        self.tile_height = self.map_data["tileheight"]

        self.tileset_data= self.map_data["tilesets"][0]

    
    def game_loop(self):
        print("in game loop")

if __name__ == "__main__":
    main=Main()
    main.game_loop()


'''
  Steps to display the map

  Step 1: Keep what you need on self.
  screen, map_data, tile_width and tile_height are local variables in __init__, so game_loop can't see them. Save them as self.screen, self.map_data and so on.

  Step 2: Load the tileset data.
  - If tileset_data has a "source" key, the tileset is external. Open map_dir / tileset_data["source"] with json.load, and keep firstgid from the map's entry.
  - If there's no "source", the tileset is embedded, and tileset_data already holds the fields you need.
  - Fields you need: image, columns, tilewidth, tileheight, tilecount, and margin / spacing (both 0 in your file).

  Step 3: Load the tileset image.
  The image path is relative to the tileset file, not your script:
  image_path = (tileset_file.parent / tileset["image"]).resolve()
  sheet = pygame.image.load(image_path).convert_alpha()
  convert_alpha() only works after set_mode() has been called. Your code already calls it first, so you're fine.

  Step 4: Cut the sheet into tiles.
  Build a dict that maps each tile's ID (its gid) to a Surface:
  for local_id in range(tilecount):
      col = local_id % columns
      row = local_id // columns
      x = margin + col * (tilewidth + spacing)
      y = margin + row * (tileheight + spacing)
      tiles[firstgid + local_id] = sheet.subsurface((x, y, tilewidth, tileheight))
  Your image is 4113 px wide, which isn't a multiple of 32. Use columns from the tileset and don't calculate it from the image width.

  Step 5: Draw the tile layer onto a map surface once.
  - Loop over map_data["layers"] and keep only those with layer["type"] == "tilelayer". Skip your objectgroup layer for now; it's for collisions later.
  - layer["data"] is a flat list of width * height gids, for example [387, 387, ..., 901, ...]. For each index i:
    - x = i % layer_width, y = i // layer_width
    - gid == 0 means an empty cell, so skip it.
    - Otherwise, blit tiles[gid] at (x * tile_width, y * tile_height).
  - Optional: gids can carry flip flags in their top bits. Clear them with gid &= 0x1FFFFFFF so the lookup can't crash.
  - Do this once onto a surface of size (map_width * tile_width, map_height * tile_height), which is 288×288 for your 9×9 map, and keep it as self.map_surface. That's much cheaper than blitting 81 tiles every frame.

  Step 6: Write the real game loop.
  running = True
  while running:
      for event in pygame.event.get():
          if event.type == pygame.QUIT:
              running = False
      self.screen.fill((0, 0, 0))
      self.screen.blit(self.map_surface, (0, 0))
      pygame.display.flip()
      self.clock.tick(60)
  pygame.quit()

  Suggested order of work

  1. Fix the tileset reference and the path, then print tileset to confirm it loads.
  2. Load the image and blit the whole sheet to the screen once to check the path.
  3. Cut the tiles and blit only tiles[387] to check your gid math.
  4. Draw the whole layer.

  After that, your next step is reading the objectgroup layer (each object has x, y, width, height) and turning it into pygame.Rect obstacles for collision.

  '''