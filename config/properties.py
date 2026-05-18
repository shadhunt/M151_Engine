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
column_starting_x = 10
column_starting_y = 25
sprite_height = 32
sprite_width = 32
sprite_separator = 1

def char_sheet_grid_formular(col_starting, row_starting, col_count=4, row_count=2 ):
   """
   #input the starting of the grid, and how many columns and rows it has, and it will return the x and y coordinates of the grid cells
   Args:
      col_starting (int): the starting column of the grid (0-indexed)
      row_starting (int): the starting row of the grid (0-indexed)
      col_count (int, optional): how many columns the grid has. Defaults to 4.
      row_count (int, optional): how many rows the grid has. Defaults to 2.
   """
   return [column_starting_x + col * (sprite_width + sprite_separator) for col in range(col_starting, col_starting + col_count)], [column_starting_y + row * (sprite_height + sprite_separator) for row in range(row_starting, row_starting + row_count)]

def char_sheet_cell_position(col, row):
   """
   #input the column and row of the cell, and it will return the x and y coordinates of the cell (top-left corner)
   """
   return column_starting_x + col * (sprite_width + sprite_separator), column_starting_y + row * (sprite_height + sprite_separator)

# Row content y-starts for the green car (rows 0 and 1 of the sheet)
# Row 0 starts at y=25, row 1 starts at y=58  (separated by a 1px line at y=57)
PLAYER_COL_X, PLAYER_ROW_Y = char_sheet_grid_formular(0, 0 , 4, 2)
MISSILE_COL_X, MISSILE_ROW_Y = char_sheet_grid_formular(4, 18, 4, 2)

COLORKEY = (32, 200, 248)   # cyan background → transparent



MISSILE_SPEED = 1100    # pixels per second for cardinal directions



SCALE = 4

ENEMY_SCALE = 3
ENEMY_SPEED = 180