"""
Game -- owns the window, the clock, and whichever Scene is currently
active.

This is the piece every earlier M151_Engine prototype was missing:
instead of each main.py hand-rolling its own pygame.init(), event loop,
and flip(), that boilerplate lives here ONCE, and any Scene just plugs
into it.

IMPORTANT: pygame.display.set_mode() must run before a Scene is
constructed, because loading images (Surface.convert()) requires a
display mode to already be set. That's why Game() takes no Scene in its
constructor -- it sets up the window first -- and the Scene is built
separately, as an argument to run():

    game = Game()          # pygame.init() + set_mode() happen here
    game.run(PlayScene())  # PlayScene() is only constructed AFTER that

Passing a Scene straight into Game's constructor instead, e.g.
`Game(PlayScene())`, would construct PlayScene() first (Python evaluates
arguments before the call) and crash the moment it tries to load an image.
"""
import pygame

from . import config


class Game:
    def __init__(self, title: str = config.TITLE):
        pygame.init()
        pygame.display.set_caption(title)
        self.screen  = pygame.display.set_mode((config.SCREEN_W, config.SCREEN_H))
        self.clock   = pygame.time.Clock()
        self.running = True
        self.scene   = None

    def run(self, scene) -> None:
        self.scene = scene
        while self.running:
            dt = self.clock.tick(config.FPS) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.scene.handle_event(event)

            self.scene.update(dt)
            self.scene.draw(self.screen)
            pygame.display.flip()

        pygame.quit()
