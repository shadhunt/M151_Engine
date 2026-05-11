class Unit():
    def __init__(self):
        print("Unit initialized")
        
    def destroyed(self):
        raise NotImplementedError
    
    def screenBoundaryCheck(self):
        raise NotImplementedError
    