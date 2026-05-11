from core.entities.entity import Entity
class Player(Entity):
    def __init__(self, world_x, world_y, frames):
        super().__init__(world_x, world_y, frames)        
