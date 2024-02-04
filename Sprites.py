from abc import ABC, abstractmethod
import Board
from copy import deepcopy
import random

class ISprites(ABC):
    def __init__(self) -> None:
        self.i = 0
        self.j = 0
  
class MovebleSprite(ISprites):
    def __init__(self) -> None:
        super().__init__()
    
    def move(self,vec,board:Board):
        new_i = self.i + vec[0]
        new_j = self.j + vec[1]
        move_is_possible = board.CanIMoveThere(new_i,new_j)
        if move_is_possible:
            self.i = new_i
            self.j = new_j
    
      
class PacMan(MovebleSprite):
    def __init__(self) -> None:
        super().__init__()
        self.live_points = 3
        self.status = "normal"
        
        
    
    
class Monster(MovebleSprite):
    def __init__(self) -> None:
        super().__init__()
        self.status = "normal"
        self.strategy = "random"
        
    def MoveStrategy(self,board:Board):
        directors_to_check = [[0,1],[0,-1],[-1,0],[1,0]] # up, down, left, right
        possible_directors = []
        for poss_vec in enumerate(directors_to_check):
            new_i = self.i + poss_vec[0]
            new_j = self.j + poss_vec[1]
            move_is_possible = board.CanIMoveThere(new_i,new_j)
            if move_is_possible: 
                possible_directors.append(deepcopy(poss_vec))
        
        if len(possible_directors)>0:
            if self.strategy == "random":
                return possible_directors[random.choice(len(possible_directors))]
            
            distance_to_pacman = 1000
            theshortes_order = [-10,-10]
            for indexp, poss_vec in enumerate(possible_directors):
                dist = board.DistanceToPacMan(poss_vec[0],poss_vec[1])
                if dist < distance_to_pacman:
                    theshortes_order[1] = theshortes_order[0]
                    theshortes_order[0] = indexp
            if self.strategy == "follow":
                return possible_directors[theshortes_order[0]]  
            elif self.strategy == "semifollow":
                return possible_directors[theshortes_order[1]]  
    
    

class NoneMovebleSprite(ISprites):
    def __init__(self) -> None:
        super().__init__() 
        
class Booster(NoneMovebleSprite):
    def __init__(self) -> None:
        super().__init__() 
        self.booster_effect = ""
        
class Coins(NoneMovebleSprite):
    def __init__(self) -> None:
        super().__init__() 
        self.coin_val = 1