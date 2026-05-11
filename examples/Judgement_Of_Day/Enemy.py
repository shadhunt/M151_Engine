from Unit import Unit
class Enemy(Unit):
    def __init__(self):
        print("Enemy initialized")
    def destroyed(self):
        print("Enemy died")
    
    def screenBoundaryCheck(self):
        print("screen boundary check")