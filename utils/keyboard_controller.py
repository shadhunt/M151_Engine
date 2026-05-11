import pygame
from config.analog_control_const import UP,UP_LEFT,LEFT,DOWN_LEFT,DOWN,DOWN_RIGHT,RIGHT,UP_RIGHT
class KeyboardController:
    '''
    - The 4 key states (up/down/left/right) are captured first, then a single     
  match on the tuple (up, down, left, right) covers all 8 directions cleanly.
  - Diagonal cases (e.g. W+A → UP_LEFT) update both x and y simultaneously.     
  - Any opposing-key combo (e.g. W+S) falls through to the _ default — no       
  movement, direction unchanged.                                                
                                                                                
  One heads-up: diagonal movement currently travels at the same per-axis step * 
  dt, which makes it ~41% faster than cardinal movement (Pythagorean effect). If
   you want equal speed in all 8 directions, multiply diagonal deltas by 0.707  
  (i.e., 1/√2). Happy to add that if needed.
  '''
    def __init__(self,step):
        self.step = step

    def actionPerform(self, x, y, current_direction, dt):
        keys  = pygame.key.get_pressed()
        up    = keys[pygame.K_w]
        down  = keys[pygame.K_s]
        left  = keys[pygame.K_a]
        right = keys[pygame.K_d]
        match (up, down, left, right):
            case (True, False, True, False):
                x -= self.step * dt * 0.707; y -= self.step * dt * 0.707
                current_direction = UP_LEFT
            case (True, False, False, True):
                x += self.step * dt * 0.707; y -= self.step * dt * 0.707
                current_direction = UP_RIGHT
            case (False, True, True, False):
                x -= self.step * dt * 0.707; y += self.step * dt * 0.707
                current_direction = DOWN_LEFT
            case (False, True, False, True):
                x += self.step * dt * 0.707; y += self.step * dt * 0.707
                current_direction = DOWN_RIGHT
            case (True, False, False, False):
                y -= self.step * dt
                current_direction = UP
            case (False, True, False, False):
                y += self.step * dt
                current_direction = DOWN
            case (False, False, True, False):
                x -= self.step * dt
                current_direction = LEFT
            case (False, False, False, True):
                x += self.step * dt
                current_direction = RIGHT

        return current_direction, x, y

    @staticmethod
    def read_keys() -> tuple[float, float, str | None]:
        """
        Poll WASD keys. Returns (dx, dy, direction_string_or_None).

        dx and dy are unit-length components of a movement direction.
        They get multiplied by speed and dt inside Entity.update().

        WHY NORMALIZE DIAGONALS?
        -------------------------
        Pure cardinal input (e.g., W only):
            dx=0, dy=-1  → magnitude = √(0²+1²) = 1.0  ✓

        Naive diagonal input (W+D):
            dx=1, dy=-1  → magnitude = √(1²+1²) = 1.414  ✗

        The entity would move 41% faster diagonally. To fix this, multiply
        diagonal components by 1/√2 ≈ 0.707, which scales them so the
        combined vector has magnitude 1.0 again:

            dx = 0.707, dy = -0.707  → magnitude = √(0.707²+0.707²) = 1.0  ✓
        """
        DIAG = 0.707   # 1 / √2

        keys = pygame.key.get_pressed()
        w = keys[pygame.K_w]
        s = keys[pygame.K_s]
        a = keys[pygame.K_a]
        d = keys[pygame.K_d]

        # Python's match statement on a tuple of booleans is a clean way to
        # handle 8-directional logic without a chain of if/elif.
        # Opposing keys (W+S or A+D) fall through to the default: no movement.
        match (w, s, a, d):
            case (True,  False, True,  False): return (-DIAG, -DIAG, "up_left")
            case (True,  False, False, True):  return ( DIAG, -DIAG, "up_right")
            case (False, True,  True,  False): return (-DIAG,  DIAG, "down_left")
            case (False, True,  False, True):  return ( DIAG,  DIAG, "down_right")
            case (True,  False, False, False): return ( 0.0,  -1.0,  "up")
            case (False, True,  False, False): return ( 0.0,   1.0,  "down")
            case (False, False, True,  False): return (-1.0,   0.0,  "left")
            case (False, False, False, True):  return ( 1.0,   0.0,  "right")
            case _:                            return ( 0.0,   0.0,  None)
