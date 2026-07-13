"""
Scene -- one screen/mode of the game (playing, paused, game-over, ...).

Game (see game.py) only knows "call update/draw/handle_event on whatever
scene is currently active." Swapping Game.scene to a different Scene
instance IS the entire mechanism for changing game state -- no
special-casing inside the main loop itself.
"""


class Scene:
    def handle_event(self, event) -> None:
        pass

    def update(self, dt: float) -> None:
        pass

    def draw(self, surface) -> None:
        pass
