from Unit import Unit
class Player(Unit):
    def destroyed(self):
        print("Player died")
    
    def screenBoundaryCheck(self):
        print("screen boundary check")