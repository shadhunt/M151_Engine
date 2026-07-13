"""
Same demo as main.py, but the level (map + enemy spawns) is loaded from
a Tiled-authored file, data/level1.tmj, instead of config.MAP_IMAGE +
data/enemies.json. See docs/M151_Tiled_Tutorial.pdf for how that file was
built, and scenes/tiled_play_scene.py for the loading code.

Run it with:
    python main_tiled_demo.py
"""
from engine.game import Game
from scenes.tiled_play_scene import TiledPlayScene

if __name__ == "__main__":
    game = Game()
    game.run(TiledPlayScene())
