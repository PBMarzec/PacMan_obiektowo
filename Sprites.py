from abc import ABC, abstractmethod

class ISprites(ABC):
    def __init__(self) -> None:
        self.i = 0
        self.j = 0
  
class MovebleSprite(ISprites):
    def __init__(self) -> None:
        super().__init__()
    
    def move(self,vec):
        self.x += vec[0]
        self.y += vec[1]
    
      
class PacMan(MovebleSprite):
    def __init__(self) -> None:
        super().__init__()
        self.live_points = 3
        self.status = "normal"
        
        
    
    
class Monster(MovebleSprite):
    def __init__(self) -> None:
        super().__init__()
        self.status = "normal"
        self.stategy = "random"
        
    def MoveStrategy(self,vec):
        pass
    
    

class NoneMovebleSprite(ISprites):
    def __init__(self) -> None:
        super().__init__() 