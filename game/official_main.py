import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


from core.game import Game
from gameplay.scenes.tiled_play_scene import TiledPlayScene

if __name__ == "__main__":
    game = Game()
    game.run(TiledPlayScene())