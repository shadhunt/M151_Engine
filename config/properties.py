# ── Display settings ─────────────────────────────────────────────────────────
SCREEN_W = 960
SCREEN_H = 540

# ── Spritesheet constants (see main_character_actions.py for full explanation)
#
# characters.png is a grid of 32×32 sprite cells separated by 1-pixel lines.
# Column x-positions start at x=10, then repeat every 33 pixels (32 + 1 sep).
# Row y-positions: row 0 starts at y=25, row 1 starts at y=58.
#
SPRITE_W  = 32
SPRITE_H  = 32

# Grid coordinates inside the spritesheet
# Column content x-starts (0-indexed): col0=10, col1=43, col2=76, col3=109
# Separator width is 1px, so spacing = 33px
COL_X    = [10 + col * 33 for col in range(4)]   # [10, 43, 76, 109]
# Row content y-starts for the green car (rows 0 and 1 of the sheet)
# Row 0 starts at y=25, row 1 starts at y=58  (separated by a 1px line at y=57)
ROW_Y = [25, 58]
COLORKEY = (32, 200, 248)   # cyan background → transparent