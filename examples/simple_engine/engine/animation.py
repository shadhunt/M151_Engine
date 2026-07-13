"""
Animator -- turns "which direction am I facing" into "which Surface do I
blit right now", and (if given more than one frame per direction)
advances a walk-cycle over time.

The art in this demo has only ONE frame per direction, so the animation
looks static -- but the class supports lists of frames per direction, so
you can drop in a real walk-cycle sheet later without touching Player or
Enemy code at all.
"""
import pygame

from . import config


class Animator:
    def __init__(self, frames: dict, fps: float = 8.0, direction: str = config.DOWN):
        """
        frames: {direction: Surface}  OR  {direction: [Surface, Surface, ...]}
        Single Surfaces are normalized into one-frame lists internally so
        update() never has to special-case "this direction has no animation".
        """
        self._frames = {
            direction: (surfaces if isinstance(surfaces, list) else [surfaces])
            for direction, surfaces in frames.items()
        }
        self._seconds_per_frame = 1.0 / fps
        self._timer = 0.0
        self._frame_index = 0
        self.direction = direction

    def set_direction(self, direction: str) -> None:
        if direction != self.direction:
            self.direction = direction
            self._frame_index = 0
            self._timer = 0.0

    def update(self, dt: float) -> None:
        frame_list = self._frames[self.direction]
        if len(frame_list) <= 1:
            return   # a single static frame -- nothing to advance
        self._timer += dt
        if self._timer >= self._seconds_per_frame:
            self._timer -= self._seconds_per_frame
            self._frame_index = (self._frame_index + 1) % len(frame_list)

    @property
    def image(self) -> pygame.Surface:
        return self._frames[self.direction][self._frame_index]
