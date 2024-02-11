from abc import ABC, abstractmethod
import Board
from copy import deepcopy
import random

class ISprites(ABC):
    def __init__(self,i,j) -> None:
        self.i = i
        self.j = j
  
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
        
    def move_pacman(self,pressed_keys:dict):
        if pressed_keys[K_UP]:
            self.move(0, 1)
        if pressed_keys[K_DOWN]:
            self.move(0, -1)
        if pressed_keys[K_LEFT]:
            self.move(-1, )
        if pressed_keys[K_RIGHT]:
            self.move(1, 0)
    
    
class Monster(MovebleSprite):
    def __init__(self,strategy="random") -> None:
        super().__init__()
        self.status = "normal"
        self.__strategy = strategy
        # self.__speed = "normal"
    
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
    booster_name_list = ["SpeedUpPacman","SickMonster"]
    def __init__(self, booster_effect_name:str) -> None:
        super().__init__() 
        self.__booster_effect = booster_effect_name
    
    @property
    def check_booster_effect(self):
        return self.__booster_effec
    
    def SpeedUpPacman(self,pacman:PacMan):
        pass
    
    def SickMonster(self,monster_set:list[Monster]):
        pass
        
class Coin(NoneMovebleSprite):
    def __init__(self) -> None:
        super().__init__() 
        self.__coin_val = 1