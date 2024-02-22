from abc import ABC, abstractmethod
import Board
from copy import deepcopy
import random
import pygame

class ISprites(ABC):
    def __init__(self,i,j) -> None:
        self.i = i
        self.j = j
  
class MovebleSprite(ISprites):
    def __init__(self,x,y) -> None:
        super().__init__(x,y)
        self.old_pos = [x,y]
    
    def move(self,vec,board:Board):
        new_i = self.i + vec[0]
        new_j = self.j + vec[1]
        move_is_possible = board.CanIMoveThere(new_i,new_j)
        if move_is_possible:
            self.old_pos = deepcopy([self.i, self.j])
            self.i = int(new_i)
            self.j = int(new_j)
    
      
class PacMan(MovebleSprite):
    def __init__(self,x,y) -> None:
        super().__init__(x,y)
        self.live_points = 3
        self.status = "normal"
                    
    def move_pacman(self,pressed_keys:pygame.key,map:Board):
        # checking if key "A" was pressed
        if pressed_keys == pygame.K_UP:
            self.move([0, 1],map)
        # checking if key "J" was pressed
        if pressed_keys == pygame.K_DOWN:
            self.move([0, -1],map)
        # checking if key "P" was pressed
        if pressed_keys == pygame.K_LEFT:
            self.move([-1, 0],map)
        # checking if key "M" was pressed
        if pressed_keys == pygame.K_RIGHT:
            self.move([1, 0],map)
    
class Monster(MovebleSprite):
    def __init__(self,x,y,strategy="random") -> None:
        super().__init__(x,y)
        self.status = "normal"
        self.__strategy = strategy
        # self.__speed = "normal"
    
    def MoveStrategy(self,board:Board):
        directors_to_check = [[0,1],[0,-1],[-1,0],[1,0]] # up, down, left, right
        possible_directors = []
        for poss_vec in directors_to_check:
            print(poss_vec)
            new_i = self.i + poss_vec[0]
            new_j = self.j + poss_vec[1]
            move_is_possible = board.CanIMoveThere(new_i,new_j)
            if move_is_possible: 
                possible_directors.append(deepcopy(poss_vec))
        
        if len(possible_directors)>0:
            if self.__strategy == "random":
                return random.choice(possible_directors)
            
            distance_to_pacman = 1000
            theshortes_order = [-10,-10]
            for indexp, poss_vec in enumerate(possible_directors):
                dist = board.DistanceToPacMan(poss_vec[0],poss_vec[1])
                if dist < distance_to_pacman:
                    theshortes_order[1] = theshortes_order[0]
                    theshortes_order[0] = indexp
            if self.__strategy == "follow":
                return possible_directors[theshortes_order[0]]  
            elif self.__strategy == "semifollow":
                return possible_directors[theshortes_order[1]]  
    
    

class NoneMovebleSprite(ISprites):
    def __init__(self,x,y) -> None:
        super().__init__(x,y) 
        
class Booster(NoneMovebleSprite):
    booster_name_list = ["SpeedUpPacman","SickMonster"]
    
    def __init__(self,x,y,) -> None:
        super().__init__(x,y) 
        self.__booster_effect = "SickMonster"
        # self.__booster_effect = deepcopy(random.choice(self.booster_name_list))
    
    @property
    def check_booster_effect(self):
        print(self.__booster_effect)
        return self.__booster_effect
    
    def SpeedUpPacman(self,pacman:PacMan):
        pass
    
    def SickMonster(self,monster_set:list[Monster]):
        for monster in monster_set:
            if monster.status == "normal":
                monster.status = "edible"
            elif monster.status == "edible":
                monster.status = "normal"
        
class Coin(NoneMovebleSprite):
    def __init__(self,x,y) -> None:
        super().__init__(x,y) 
        self.__coin_val = 1