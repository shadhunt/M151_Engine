from Unit import Unit
class Player(Unit):
    def __init__(self):
        print("Player initialized")
    def destroyed(self):
        print("Player died")
    
    def screenBoundaryCheck(self):
        print("screen boundary check")