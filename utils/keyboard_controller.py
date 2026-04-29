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
                x -= self.step * dt; y -= self.step * dt
                current_direction = UP_LEFT
            case (True, False, False, True):
                x += self.step * dt; y -= self.step * dt
                current_direction = UP_RIGHT
            case (False, True, True, False):
                x -= self.step * dt; y += self.step * dt
                current_direction = DOWN_LEFT
            case (False, True, False, True):
                x += self.step * dt; y += self.step * dt
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