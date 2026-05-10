from engine.entities.entity import Entity
class Player(Entity):
    def __init__(self, name, health, position):
        super().__init__(health, position)
        self.name = name
