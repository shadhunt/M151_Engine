"""
Entry point for the Simple Engine demo.

Run it with:
    python main.py                             (from this folder)
    python examples/simple_engine/main.py       (from anywhere else)

Both work because Python always puts the launched script's own directory
first on sys.path, so `engine`, `entities`, and `scenes` resolve as
packages either way -- no path hacking needed.

See README.md in this folder, and the PDF guide in docs/, for a tour of
how the pieces fit together and ideas for what to build next.
"""
from engine.game import Game
from scenes.play_scene import PlayScene

if __name__ == "__main__":
    game = Game()          # sets up the window first...
    game.run(PlayScene())  # ...so PlayScene can safely load images
