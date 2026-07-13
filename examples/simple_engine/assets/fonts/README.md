# fonts/

Empty on purpose -- `PlayScene._draw_hud()` currently uses
`pygame.font.SysFont("monospace", 16)`, a font installed on the OS, so no
font file ships with the project.

`SysFont` is fine for a debug HUD but is NOT reliable for a real game:
the exact font differs between your machine and anyone else who runs the
project, so text can wrap or overflow differently on their screen.

To make the HUD/UI look the same everywhere:

1. Drop a `.ttf` file in here (many free bitmap/pixel fonts fit an
   8-bit tank game well).
2. Replace `pygame.font.SysFont(...)` with
   `pygame.font.Font(config.ASSETS_DIR / "fonts" / "your_font.ttf", 16)`.
3. Reuse that one `Font` object everywhere instead of creating a new one
   per Scene -- loading a font file is not free.
