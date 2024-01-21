from abc import ABC, abstractmethod

class ISprites(ABC):
    def __init__(self) -> None:
        self.i = 0
        self.j = 0
  
class MovebleSprite(ISprites):
    def __init__(self) -> None:
        super().__init__()
    
    @abstractmethod
    def move(self,vec):
        pass

class NoneMovebleSprite(ISprites):
    def __init__(self) -> None:
        super().__init__()     
      
class PacMan(MovebleSprite):
    def __init__(self) -> None:
        super().__init__()
        self.live_points = 3
        
    def move(self,vec):
        pass
    
    
class Monster(MovebleSprite):
    def __init__(self) -> None:
        super().__init__()
        self.status = "normal"
        self.stategy = "random"
        
    def move(self,vec):
        pass