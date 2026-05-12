from config.properties import MISSILE_SPEED
UP_LEFT    = "up_left"
UP         = "up"
UP_RIGHT   = "up_right"
RIGHT      = "right"
LEFT       = "left"
DOWN_LEFT  = "down_left"
DOWN       = "down"
DOWN_RIGHT = "down_right"

# Maps each player direction string to its (sheet_row, sheet_col) in characters.png
PLAYER_DIRECTION_COORDS = {
    UP_LEFT:    (0, 0),
    UP:         (0, 1),
    UP_RIGHT:   (0, 2),
    RIGHT:      (0, 3),
    LEFT:       (1, 0),
    DOWN_LEFT:  (1, 1),
    DOWN:       (1, 2),
    DOWN_RIGHT: (1, 3),
}



# Missile — rows 18-19, cols 4-7 (0-based)  ←  art-file rows 19-20, cols 5-8 (1-based)
_S = MISSILE_SPEED
_D = MISSILE_SPEED * 0.707   # diagonal speed: same actual distance per second

MISSILE_COORDS = {
    UP_LEFT:    (18, 4),
    UP:         (18, 5),
    UP_RIGHT:   (18, 6),
    RIGHT:      (18, 7),
    LEFT:       (19, 4),
    DOWN_LEFT:  (19, 5),
    DOWN:       (19, 6),
    DOWN_RIGHT: (19, 7),
}

# velocity (vx, vy) in pixels-per-second for each direction
VELOCITY_MAP = {
    UP:         ( 0,  -_S),
    DOWN:       ( 0,  +_S),
    LEFT:       (-_S,  0),
    RIGHT:      (+_S,  0),
    UP_LEFT:    (-_D, -_D),
    UP_RIGHT:   (+_D, -_D),
    DOWN_LEFT:  (-_D, +_D),
    DOWN_RIGHT: (+_D, +_D),
}
