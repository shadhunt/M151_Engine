import pygame
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

    UP_LEFT    = "up_left"
    UP         = "up"
    UP_RIGHT   = "up_right"
    RIGHT      = "right"
    LEFT       = "left"
    DOWN_LEFT  = "down_left"
    DOWN       = "down"
    DOWN_RIGHT = "down_right"
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
                current_direction = self.UP_LEFT
            case (True, False, False, True):
                x += self.step * dt; y -= self.step * dt
                current_direction = self.UP_RIGHT
            case (False, True, True, False):
                x -= self.step * dt; y += self.step * dt
                current_direction = self.DOWN_LEFT
            case (False, True, False, True):
                x += self.step * dt; y += self.step * dt
                current_direction = self.DOWN_RIGHT
            case (True, False, False, False):
                y -= self.step * dt
                current_direction = self.UP
            case (False, True, False, False):
                y += self.step * dt
                current_direction = self.DOWN
            case (False, False, True, False):
                x -= self.step * dt
                current_direction = self.LEFT
            case (False, False, False, True):
                x += self.step * dt
                current_direction = self.RIGHT

        return current_direction, x, y