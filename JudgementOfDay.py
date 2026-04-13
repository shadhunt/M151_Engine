from Player import Player
from Enemy import Enemy
def allDie(unit):
    unit.destroyed()

if __name__ == "__main__":
    player = Player
    enemy = Enemy
    allDie(player)
    allDie(enemy)