from copy import deepcopy
from pathlib import Path
import math

class Board:
    def __init__(self,boardfile:Path) -> None:
        self.__map = self.ImportMap(boardfile)
        self.__PacManPossition = []
    
    TypeOfTiles = {"#":"Wall",
                    "P":"PacMan",
                    "F":"Food",
                    "M":"Monster"}
    
    def ImportMap(self,file)->list[list]:
        Map = []
        with open(file, 'r') as mapfile:
            all_lines = mapfile.readlines()
            for line in all_lines:
                one_line = line.split() 
                one_map_row = [self.TypeOfTiles[x] for x in one_line]
                Map.append(deepcopy(one_map_row))
        return deepcopy(Map)
    
    def DrowBoard(self):
        pass
    
    def UpdateBoard(self):
        pass
    
    def Colitions(self,one_sprite, second_sprite):
        pass
    
    @property
    def WhatIsHere(self,col,row):
        return self.map[row][col] 
    
    @property
    def CanIMoveThere(self,x,y):
        if self.map[x][y] == "Wall":
            return False
        else:
            return True
    
    @property
    def DistanceToPacMan(self,x,y):
        distance = math.sqrt((self.__PacManPossition[0]-x)**2+(self.__PacManPossition[1]-y)**2)
        return distance
    
class OneTile:
    def __init__(self,tile_type:str,board_mode="normal") -> None:
        self.type = tile_type
        self.pic = ""
        self.board_mode = board_mode
        
        if self.board_mode == "normal":
            pass
        
        
        