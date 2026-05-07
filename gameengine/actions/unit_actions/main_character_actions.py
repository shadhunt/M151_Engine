"""
main_character.py

Loads the green car (first 2 rows, first 4 columns) from characters.png
and builds a direction → pygame.Surface map.

Spritesheet layout (characters.png):
  - Each cell is 32×32 pixels
  - Cells are separated by 1-pixel magenta grid lines
  - Column content starts at x=10, spaced every 33 pixels
  - Row 0 content starts at y=25; Row 1 content starts at y=58

Direction map (green car = row 0–1, col 0–3):

  Row 0:  col0=UP_LEFT  col1=UP   col2=UP_RIGHT  col3=RIGHT
  Row 1:  col0=LEFT     col1=DOWN_LEFT  col2=DOWN  col3=DOWN_RIGHT
"""
import sys
from pathlib import Path

isDebug = True
if isDebug:
    print("project path is:"+str(Path(__file__).parent.parent.parent.parent))
sys.path.append(str(Path(__file__).parent.parent.parent.parent))
import os
import pygame
from pygame.surface import Surface
import config.path_config as path_config
from config.analog_control_const import UP, _DIRECTION_COORDS


# Path relative to this file
#_SHEET_PATH = os.path.join(os.path.dirname(__file__), "assets", "characters", "characters.png") #this is not the best way to locate file
#_SHEET_PATH = (Path(__file__).parent.parent / "assets"/ "characters"/ "characters.png") #this is the best way to locate file

'''
this is the way without path config
_SHEET_PATH = (Path(__file__).parent.      #in action
        parent                             #in project_root
        / "assets"   
        / "characters"
        / "characters.png")

'''

_SHEET_PATH = path_config.ASSETS_DIR / "characters" / "characters.png"
# Sprite dimensions
SPRITE_W = 32
SPRITE_H = 32

# Grid coordinates inside the spritesheet
# Column content x-starts (0-indexed): col0=10, col1=43, col2=76, col3=109
# Separator width is 1px, so spacing = 33px
_COL_X = [10 + col * 33 for col in range(4)]   # [10, 43, 76, 109]

# Row content y-starts for the green car (rows 0 and 1 of the sheet)
# Row 0 starts at y=25, row 1 starts at y=58  (separated by a 1px line at y=57)
_ROW_Y = [25, 58]

# Maps direction → (sheet_row, sheet_col)



def load_character_frames() -> dict[str, pygame.Surface]:
    """
    Loads the spritesheet and returns a dict mapping each direction
    constant to its cropped 32×32 pygame.Surface.

    Returns:
        {
            "up_left":    <Surface>,
            "up":         <Surface>,
            "up_right":   <Surface>,
            "right":      <Surface>,
            "left":       <Surface>,
            "down_left":  <Surface>,
            "down":       <Surface>,
            "down_right": <Surface>,
        }
    """
    sheet = pygame.image.load(_SHEET_PATH).convert_alpha()

    frames = {}
    for direction, (row, col) in _DIRECTION_COORDS.items():
        x = _COL_X[col]
        y = _ROW_Y[row]
        rect = pygame.Rect(x, y, SPRITE_W, SPRITE_H)
        #frame = pygame.Surface((SPRITE_W, SPRITE_H), pygame.SRCALPHA) #conflict with set_colorkey below
        frame = pygame.Surface((SPRITE_W, SPRITE_H))
        frame.blit(sheet, (0, 0), rect)
        frame.set_colorkey((32, 200, 248))   # make cyan background transparent
        frames[direction] = frame

    return frames

def get_direction(scale,frames, direction:str):
    if isDebug:
        print(f"direction received: '{direction}'")                                                                                                                                                                                                                                                                                 
        print(f"valid keys: {list(_DIRECTION_COORDS.keys())}")  

    scaled = pygame.transform.scale(frames[direction], (SPRITE_W * scale, SPRITE_H * scale))
    '''
    ● It takes the small 32×32 sprite and enlarges it for display.                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                                                                              
    Breaking it down piece by piece:            
                                                                                                                                                                                                                                                                                                                                
    - frames[direction] — looks up the sprite for the current direction in your dictionary. For example if direction = "up", it fetches the 32×32 surface of the car facing up.                                                                                                                                                 
    - (SPRITE_W * scale, SPRITE_H * scale) — calculates the new size. SPRITE_W = 32, scale = 4, so 32 * 4 = 128. The new size is (128, 128).                                                                                                                                                                                    
    - pygame.transform.scale(...) — stretches the 32×32 surface to 128×128.
    - scaled = — stores the enlarged surface so it can be returned and drawn on screen.                                                                                                                                                                                                                                         
                                                
    So in plain English: "take the tiny sprite for this direction and zoom it up 4x so it's visible on screen."                                                                                                                                                                                                                 
                                            
    Without this line, the car would be drawn as a tiny 32×32 pixel square — barely visible on a modern screen
    '''
    return scaled

#def show_character_direction(screen:Surface,layout:list[list[str]],direction_num):

    

## this method is for testing the cutting and display of art asset
'''          
  The big picture first                                                                                                                                                                                                                                                                                                       
                                                                                                                                                                                                                                                                                                                              
  The test screen draws 8 car sprites arranged in a 4-column × 2-row grid, each with a text label underneath. Every variable is serving that layout.                                                                                                                                                                          
                                                                                                                                                                                                                                                                                                                              
  ---             
  scale = 4                                                                                                                                                                                                                                                                                                                   
                  
  The sprites are only 32×32 pixels — tiny on a modern screen. scale zooms them up before drawing.
  32 × 4 = 128 pixels wide/tall on screen                                                                                                                                                                                                                                                                                     
  Without it you'd barely see the cars.  
                                                                                                                                                                                                                                                                                                                              
  ---                                                                                                                                                                                                                                                                                                                         
  padding = 10
                                                                                                                                                                                                                                                                                                                              
  The gap (in pixels) between sprites and between sprites and the window edge. It's the "margin/gutter" of the grid.
                                                                                                                                                                                                                                                                                                                              
  ---
  label_h = 20                                                                                                                                                                                                                                                                                                                
                  
  Each cell needs space below the sprite for the text label (e.g. "up left"). label_h reserves 20 pixels for that text row so sprites don't overlap their labels.
                                                                                                                                                                                                                                                                                                                              
  ---
  x and y                                                                                                                                                                                                                                                                                                                     
                  
  These are calculated fresh for each cell inside the loop — they are the pixel coordinates of where to draw each sprite on the screen.
                                                                                                                                                                                                                                                                                                                              
  x = padding + c * (SPRITE_W * scale + padding)
  y = padding + r * (SPRITE_H * scale + padding + label_h)                                                                                                                                                                                                                                                                    
                  
  - c is the column index (0–3), r is the row index (0–1)                                                                                                                                                                                                                                                                     
  - Each step moves right by one sprite-width + one padding gap
  - Each step moves down by one sprite-height + label space + one padding gap                                                                                                                                                                                                                                                 
                                                                                                                                                                                                                                                                                                                              
  Visually:                                                                                                                                                                                                                                                                                                                   
  padding  [sprite+label]  padding  [sprite+label]  padding ...                                                                                                                                                                                                                                                               
                  
  ---                                                                                                                                                                                                                                                                                                                         
  frames
                                                                                                                                                                                                                                                                                                                              
  This is the dictionary returned by load_character_frames() — it maps each direction name to its cropped pygame.Surface:
                                                                                                                                                                                                                                                                                                                              
  frames = {
      "up_left":    <Surface 32x32>,                                                                                                                                                                                                                                                                                          
      "up":         <Surface 32x32>,
      "up_right":   <Surface 32x32>,                                                                                                                                                                                                                                                                                          
      "right":      <Surface 32x32>,
      "left":       <Surface 32x32>,                                                                                                                                                                                                                                                                                          
      "down_left":  <Surface 32x32>,
      "down":       <Surface 32x32>,                                                                                                                                                                                                                                                                                          
      "down_right": <Surface 32x32>,
  }                                                                                                                                                                                                                                                                                                                           
                  
  Think of it as your sprite bank — you ask it for a direction, it gives you the image.                                                                                                                                                                                                                                       
  
  ---                                                                                                                                                                                                                                                                                                                         
  direction       
                                                                                                                                                                                                                                                                                                                              
  The loop variable that holds the current direction string as the loops iterate through layout:
                                                                                                                                                                                                                                                                                                                              
  layout = [      
      [UP_LEFT,  UP,        UP_RIGHT,  RIGHT],   # row 0                                                                                                                                                                                                                                                                      
      [LEFT,     DOWN_LEFT, DOWN,      DOWN_RIGHT]  # row 1                                                                                                                                                                                                                                                                   
  ]
                                                                                                                                                                                                                                                                                                                              
  On the first iteration: direction = "up_left" → used to fetch frames["up_left"] and to render the text label "up left".                                                                                                                                                                                                     
  
  ---                                                                                                                                                                                                                                                                                                                         
  How they all connect in one cell
                                                                                                                                                                                                                                                                                                                              
  # e.g. r=0, c=1  →  the "up" sprite
  x = 10 + 1 * (32*4 + 10) = 148        # 2nd column position                                                                                                                                                                                                                                                                 
  y = 10 + 0 * (32*4 + 20 + 10) = 10    # 1st row position                                                                                                                                                                                                                                                                    
  direction = "up"                                                                                                                                                                                                                                                                                                            
  scaled = scale frames["up"] to 128x128                                                                                                                                                                                                                                                                                      
  draw scaled sprite at (148, 10)                                                                                                                                                                                                                                                                                             
  draw label "up" at (148, 10 + 128 + 2)
'''

def show_direction(screen:Surface, layout:list[list[str]],direction_index:int):
    print(_DIRECTION_COORDS(direction_index))

def show_character_test_screen(screen:Surface,layout:list[list[str]],frames, font, padding,scale, label_h):
    for r, row_dirs in enumerate(layout):
        for c, direction in enumerate(row_dirs):
            x = padding + c * (SPRITE_W * scale + padding)
            y = padding + r * (SPRITE_H * scale + padding + label_h)

            scaled = pygame.transform.scale(frames[direction], (SPRITE_W * scale, SPRITE_H * scale))
            screen.blit(scaled, (x, y))

            label = font.render(direction.replace("_", " "), True, (220, 220, 220))
            screen.blit(label, (x, y + SPRITE_H * scale + 2))


# ---------------------------------------------------------------------------
# Quick visual test – run this file directly to verify all 8 frames
# ---------------------------------------------------------------------------
if __name__ == "__main__":

    pygame.init()
    scale = 4  # zoom factor for visibility

    cols, rows = 4, 2
    padding = 10
    label_h = 20
    win_w = cols * (SPRITE_W * scale + padding) + padding
    win_h = rows * (SPRITE_H * scale + padding + label_h) + padding

    screen = pygame.display.set_mode((win_w, win_h))
    pygame.display.set_caption("Main Character – Direction Map")
    font = pygame.font.SysFont(None, 18)

    frames = load_character_frames()

    # Layout order matches the spritesheet visually
    layout = [
        [UP_LEFT, UP, UP_RIGHT, RIGHT],
        [LEFT, DOWN_LEFT, DOWN, DOWN_RIGHT],
    ]

    screen.fill((120, 111, 77))
    show_character_test_screen(screen, layout, frames, font, padding, scale,label_h)
    '''
    for r, row_dirs in enumerate(layout):
        for c, direction in enumerate(row_dirs):
            x = padding + c * (SPRITE_W * scale + padding)
            y = padding + r * (SPRITE_H * scale + padding + label_h)

            scaled = pygame.transform.scale(frames[direction], (SPRITE_W * scale, SPRITE_H * scale))
            screen.blit(scaled, (x, y))

            label = font.render(direction.replace("_", " "), True, (220, 220, 220))
            screen.blit(label, (x, y + SPRITE_H * scale + 2))
    '''
    pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                running = False

    pygame.quit()

