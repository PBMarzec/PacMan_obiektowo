from copy import deepcopy

class Board:
    def __init__(self,boardfile:__path__) -> None:
        self.__map = self.ImportMap(boardfile)
    
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
    
    def UpdateBoard():
        pass
    
    def Colitions():
        pass
    
    @property
    def WhatIsHere(self,col,row):
        return self.map[row][col] 
    
class OneTile:
    def __init__(self) -> None:
        self.type = ""
        self.pic = ""
        pass