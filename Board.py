from copy import deepcopy
from pathlib import Path
import math
import pygame
import main
import Sprites
import random

pygame.init()

class Board():
    def __init__(self,map_list:list,Pacman:Sprites.PacMan,screen:pygame) -> None:
        self.__map = []
        self.__screen = screen
        self.__PacManPossition = []
        self.__active_monster = []
        self.__active_food = []
        self.__active_coins = []
        self.__Total_points = 0
    
        self.ImportMap(map_list,Pacman)
    
    def ImportMap_copy(self,map_list,pacman:Sprites.PacMan)->list[list]:
        TypeOfTiles = {"#":"Wall",
                    "P":"PacMan",
                    "F":"Food",
                    "M":"Monster",
                    " ":"Coin"}
        
        for indexcol, line in enumerate(map_list):
            one_line = list(line)
            one_map_row = []
            for indexrow, x in enumerate(one_line[:-1]):
                one_map_row.append((OneTile(tile_type=TypeOfTiles[x])))
                if x == 'M':
                    self.__active_monster.append((Sprites.Monster(indexrow,
                                                                            indexcol,
                                                                            strategy="random")))
                elif x == 'P':
                    self.__PacManPossition = indexrow,indexcol
                    pacman.i = indexcol
                    pacman.i = indexrow
                elif x == 'F':
                    self.__active_food.append((Sprites.Booster(indexrow,
                                                                        indexcol,
                                                                        random(Sprites.Booster.booster_name_list))))
                elif x == ' ':
                    self.__active_coins.append((Sprites.Coin(indexrow,indexcol)))
            self.__map.append((one_map_row))
    
    def ImportMap(self,map_list,pacman:Sprites.PacMan)->list[list]:
        for indexcol, line in enumerate(map_list):
            one_line = list(line)
            one_map_row = []
            for indexrow, x in enumerate(one_line[:-1]):
                one_tile = OneTile(x)
                one_map_row.append((one_tile))
                if one_tile.type == 'Monster':
                    self.__active_monster.append((Sprites.Monster(indexrow,
                                                                            indexcol,
                                                                            strategy="random")))
                elif one_tile.type == 'PacMan':
                    self.__PacManPossition = indexrow,indexcol
                    pacman.i = indexcol
                    pacman.i = indexrow
                elif one_tile.type == 'Food':
                    self.__active_food.append((Sprites.Booster(indexrow,
                                                                        indexcol,
                                                                        random(Sprites.Booster.booster_name_list))))
                elif one_tile.type == 'Coin':
                    self.__active_coins.append((Sprites.Coin(indexrow,indexcol)))
            self.__map.append((one_map_row))
                            
    
    @property
    def active_monster(self)->list[Sprites.Monster]:
        return self.__active_monster
    
    
    def DrowBoard(self):
        for indexr, row in enumerate(self.__map):
            for indexc, col in enumerate(row):
                self.__screen.blit(col.pic,(indexc*20,indexr*20))
        pygame.display.flip()
    
    def UpdateBoard(self,pacman_obiect):
        for monster in self.__active_monster:
            self.__map(monster.j,monster.i).type = "Monster"
            self.__map(monster.old_pos[0],monster.old_pos[1]).type = "Path"
            if monster.j == pacman_obiect.j and monster.i == pacman_obiect.i:
                self.Colitions(pacman_obiect,monster)
        for food in self.__active_food:
            if food.j == pacman_obiect.j and food.i == pacman_obiect.i:
                self.Colitions(pacman_obiect,food)
        for food in self.__active_food:
            if food.j == pacman_obiect.j and food.i == pacman_obiect.i:
                self.Colitions(pacman_obiect,food)
        self.__map(pacman_obiect.j,pacman_obiect.i).type = "PacMan"
        self.__map(pacman_obiect.old_pos[0],pacman_obiect.old_pos[1]).type = "Path"
        self.__PacManPossition = [pacman_obiect.j,pacman_obiect.i]
             
        
    
    @staticmethod
    def send_gameover():
        main.running = False
        
        
    @staticmethod
    def determine_which_pacman_monster_food(one_sprite:Sprites.ISprites, 
                                          second_sprite:Sprites.ISprites) -> tuple[Sprites.PacMan,
                                                                                    Sprites.Booster]:
        PacManObiect = None
        MonsterObiect = None
        FoodObiect = None
        if isinstance(one_sprite, Sprites.PacMan):
            PacManObiect = one_sprite
        if isinstance(second_sprite, Sprites.PacMan):
            PacManObiect = second_sprite
        if isinstance(one_sprite, Sprites.Booster):
            FoodObiect = one_sprite
        if isinstance(second_sprite, Sprites.Booster):
            FoodObiect = second_sprite
        if isinstance(one_sprite, Sprites.Monster):
            MonsterObiect = one_sprite
        if isinstance(second_sprite, Sprites.Monster):
            MonsterObiect = second_sprite
        return PacManObiect, MonsterObiect, FoodObiect
        
        
    def PacMan_vs_Monster(self,pacman_obiect:Sprites.PacMan, 
                          monster_obiect:Sprites.Monster):
        if monster_obiect.status == "normal":
            self.send_gameover()     
        elif monster_obiect.status == "edible":
            monster_obiect.__del__()
            self.__Total_points += 100
    
    
    def PacMan_vs_Food(self,pacman_obiect:Sprites.PacMan, 
                          food_obiect:Sprites.Booster,
                          monster_set:list[Sprites.Monster]):
        if food_obiect.check_booster_effect() == "SpeedUpPacman":
            food_obiect.SpeedUpPacman(pacman_obiect) 
        elif food_obiect.check_booster_effect() == "SickMonster":
            food_obiect.SickMonster(monster_set=monster_set) 
        
    
    
    def ColectCoin(self):
        self.__Total_points += 1 
        
        
    @staticmethod
    def DoNothing():
        pass
        
    
    def Colitions(self,one_sprite, second_sprite):
        pacman_object, monster_object, food_object = self.determine_which_monster_which_pacman(one_sprite,second_sprite)
        
        colition_dict = {("PacMan","Monster"):self.PacMan_vs_Monster(pacman_object,
                                                                     monster_object),
                         ("PacMan","Booster"):self.PacMan_vs_Food(pacman_object,
                                                                  food_object,
                                                                  self.__active_monster),
                         ("PacMan","Coin"):self.ColectCoin(),
                         ("Monster","PacMan"):self.PacMan_vs_Monster(pacman_object,
                                                                     monster_object),
                         ("Monster","Booster"):self.DoNothing(),
                         ("Monster","Coin"):self.DoNothing()}
        
        colition_dict[(one_sprite.__class__.__name__,
                                second_sprite.__class__.__name__)]
        
    
    
    def WhatIsHere(self,col,row):
        return self.__map[row][col] 
    
    def CanIMoveThere(self,x,y):
        print(f"number of rows: {len(self.__map)}, number of columnes: {len(self.__map[1])}, x: {x}, y: {y}")
        if 0 <= x < len(self.__map[1]) and  0 <= y < len(self.__map):
            if self.__map[y-1][x-1] == "Wall":
                return False
            else:
                return True
        else: 
            return False
    
    @property
    def DistanceToPacMan(self,x,y):
        distance = math.sqrt((self.__PacManPossition[0]-x)**2+(self.__PacManPossition[1]-y)**2)
        return distance
    
class OneTile_copy:
    def __init__(self,tile_type:str,board_mode="normal") -> None:
        self.type = tile_type
        self.pic = ""
        self.board_mode = board_mode
        
        if self.board_mode == "normal":
            normal_pic_dict = {"Wall":"./pic/normal_wall.jpg",
                               "PacMan":"./pic/normal_pacman.jpg",
                                "Food":"./pic/normal_food.jpg",
                                "Monster":"./pic/normal_monster.jpg",
                                "Path":"./pic/normal_path.jpg",
                                "Coin":"./pic/normal_coin.jpg"}
            self.pic = pygame.image.load(normal_pic_dict[self.type])
    
    def update_pic(self):
        old_type = self.normal_pic_dict.keys()[self.pic]
        if old_type != self.type:
            self.pic = pygame.image.load(self.normal_pic_dict[self.type])

 
        
class OneTile:
    TypeOfTiles = {"#":"Wall",
                    "P":"PacMan",
                    "F":"Food",
                    "M":"Monster",
                    " ":"Coin"}
    normal_pic_dict = {"Wall":"./pic/normal_wall.jpg",
                        "PacMan":"./pic/normal_pacman.jpg",
                        "Food":"./pic/normal_food.jpg",
                        "Monster":"./pic/normal_monster.jpg",
                        "Path":"./pic/normal_path.jpg",
                        "Coin":"./pic/normal_coin.jpg"}
    
    def __init__(self,tile_string:str,board_mode="normal") -> None:
        self.type = ""
        self.pic = ""
        self.board_mode = board_mode
        
        self.type = self.TypeOfTiles[tile_string]
        self.choose_board_theme_and_pic()  
        
     
    @staticmethod       
    def choose_pic(pic_type, pic_path):
        if pic_type == "Wall":
            return WallPic(pic_type, pic_path)
        elif pic_type == "PacMan":
            return PacManPic(pic_type, pic_path)
        elif pic_type == "Food":
            return FoodPic(pic_type, pic_path)
        elif pic_type == "Monster":
            return MonsterPic(pic_type, pic_path)
        elif pic_type == "Path":
            return PathPic(pic_type, pic_path)
        elif pic_type == "Coin":
            return CoinPic(pic_type, pic_path)
        else:
            print(f"Error - choose_pic function don't know this key {pic_type}")
            
    def choose_board_theme_and_pic(self):
        if self.board_mode == "normal":
            self.pic = self.choose_pic(self.type,self.normal_pic_dict[self.type])
        
        
    def update_pic(self):
        old_type = self.normal_pic_dict.keys()[self.pic]
        if old_type != self.type:
            self.choose_board_theme_and_pic()


class PictureClass:
    def __init__(self,pic_type:str,pic_path:str) -> None:
        self.type = pic_type
        self.pic = pygame.image.load(pic_path)    
        
class WallPic(PictureClass):
    def __init__(self,pic_type:str,pic_path:str) -> None:
        self.type = pic_type
        super().__init__(pic_path)
                
class PacManPic(PictureClass):
    def __init__(self,pic_type:str,pic_path:str) -> None:
        self.type = pic_type
        super().__init__(pic_path)
                
class FoodPic(PictureClass):
    def __init__(self,pic_type:str,pic_path:str) -> None:
        self.type = pic_type
        super().__init__(pic_path)
                
class MonsterPic(PictureClass):
    def __init__(self,pic_type:str,pic_path:str) -> None:
        self.type = pic_type
        super().__init__(pic_path)
            
class CoinPic(PictureClass):
    def __init__(self,pic_type:str,pic_path:str) -> None:
        self.type = pic_type
        super().__init__(pic_path)
                
class PathPic(PictureClass):
    def __init__(self,pic_type:str,pic_path:str) -> None:
        self.type = pic_type
        super().__init__(pic_path)
                