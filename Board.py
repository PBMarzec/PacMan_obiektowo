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
        self.__game_running = True
    
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
        for indexrow, line in enumerate(map_list):
            one_line = list(line)
            one_map_row = []
            for indexcol, x in enumerate(one_line[:-1]):
                one_tile = OneTile(x)
                one_map_row.append((one_tile))
                if one_tile.type == 'Monster':
                    self.__active_monster.append((Sprites.Monster(indexcol,indexrow,
                                                                  strategy="random")))
                elif one_tile.type == 'PacMan':
                    self.__PacManPossition = indexrow,indexcol
                    pacman.i = indexcol
                    pacman.j = indexrow
                elif one_tile.type == 'Food':
                    self.__active_food.append((Sprites.Booster(indexcol,indexrow)))
                elif one_tile.type == 'Coin':
                    self.__active_coins.append((Sprites.Coin(indexcol,indexrow)))
            self.__map.append((one_map_row))
                            
    
    @property
    def active_monster(self)->list[Sprites.Monster]:
        return self.__active_monster
    
    
    def DrowBoard(self):
        for indexr, row in enumerate(self.__map):
            for indexc, col in enumerate(row):
                self.__screen.blit(col.pic,(indexc*20,indexr*20))
        pygame.display.flip()
    
    def DrawGameOver(self):
        # darkblue = (0, 0, 139, 255)
        # white = (255, 255, 255, 255)
        self.__screen.fill("darkblue")
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render(f"Game Over \n Total Score: {self.__Total_points}", True, "white")
        textRect = text.get_rect()
        textRect.center = (len(self.__map[1])*20//2, len(self.__map)*20//2)
        self.__screen.blit(text, textRect)
        # self.__screen.draw_text(f"Game Over\nTotal Score: {self.__Total_points}", white)
        # text_surface = FONT.render("Press space bar to play again", True, WHITE)
        # self.screen.blit(text_surface, (WIDTH / 2, HEIGHT * 7 / 8))
        pygame.display.flip()

    
    
    
    def UpdateBoard(self,pacman_obiect):
        print(f"\nUpdateBoard: number of rows: {len(self.__map)}, number of columnes: {len(self.__map[1])}")
        
        for monster in self.__active_monster:
            print (f"Monster: {self.__active_monster.index(monster)}, monster.j: {monster.j}, monster.i: {monster.i} ")
            if monster.status == "normal":
                self.__map[monster.j][monster.i].update_pic("Monster")
            elif monster.status == "edible":
                self.__map[monster.j][monster.i].update_pic("Monster_sick")
            for coin in self.__active_coins:
                if coin.i == monster.old_pos[0] and coin.j == monster.old_pos[1]:
                    self.__map[monster.old_pos[1]][monster.old_pos[0]].update_pic("Coin")
                else:
                    self.__map[monster.old_pos[1]][monster.old_pos[0]].update_pic("Path")
            if monster.i == pacman_obiect.i and monster.j == pacman_obiect.j :
                print(f"len(self.__active_monster): {len(self.__active_monster)}")
                self.Colitions(pacman_obiect,monster)
                print(f"len(self.__active_monster): {len(self.__active_monster)}")
                
        for food in self.__active_food:
            if food.i == pacman_obiect.i and food.j == pacman_obiect.j :
                self.Colitions(pacman_obiect,food)
        if len(self.__active_coins)>0:
            for coin in self.__active_coins:
                if coin.i == pacman_obiect.i and coin.j == pacman_obiect.j :
                    print(f"len(self.__active_coins): {len(self.__active_coins)}")
                    self.Colitions(pacman_obiect,coin)
                    print(f"len(self.__active_coins): {len(self.__active_coins)}")
        else:
            self.__game_running = False
                
        print (f"PacMan: pacman.j: {pacman_obiect.j}, pacman.i: {pacman_obiect.i} ")
        print (f"PacMan: pacman.old_j: {pacman_obiect.old_pos[1]}, pacman.old_i: {pacman_obiect.old_pos[0]} ")
        self.__map[pacman_obiect.j][pacman_obiect.i].update_pic("PacMan")
        self.__map[pacman_obiect.old_pos[1]][pacman_obiect.old_pos[0]].update_pic("Path")
        self.__PacManPossition = [pacman_obiect.j,pacman_obiect.i]
        if self.__game_running:
            return "game"
        else:
            return "the end"
        
    @staticmethod
    def determine_which_pacman_monster_food(one_sprite:Sprites.ISprites, 
                                          second_sprite:Sprites.ISprites) -> tuple[Sprites.PacMan,
                                                                                    Sprites.Booster]:
        PacManObject = None
        MonsterObject = None
        FoodObject = None
        CoinObject = None
        if isinstance(one_sprite, Sprites.PacMan):
            print(f"one_sprite is PacMan")
            PacManObject = one_sprite
        if isinstance(second_sprite, Sprites.PacMan):
            print(f"second_sprite is PacMan")
            PacManObject = second_sprite
        if isinstance(one_sprite, Sprites.Booster):
            print(f"one_sprite is Booster")
            FoodObject = one_sprite
        if isinstance(second_sprite, Sprites.Booster):
            print(f"second_sprite is Booster")
            FoodObject = second_sprite
        if isinstance(one_sprite, Sprites.Monster):
            print(f"one_sprite is Monster")
            MonsterObject = one_sprite
        if isinstance(second_sprite, Sprites.Monster):
            print(f"second_sprite is Monster")
            MonsterObject = second_sprite
        if isinstance(one_sprite, Sprites.Coin):
            print(f"one_sprite is Coin")
            CoinObject = one_sprite
        if isinstance(second_sprite, Sprites.Coin):
            print(f"second_sprite is Coin")
            CoinObject = second_sprite
        return PacManObject, MonsterObject, FoodObject, CoinObject
        
        
    def PacMan_vs_Monster(self,pacman_obiect:Sprites.PacMan, 
                          monster_obiect:Sprites.Monster):
        print("!!!!!!!!!!!!!! PacMan_vs_Monster !!!!!!!!!!!!!!!!")
        if monster_obiect.status == "normal":
            self.__game_running = False
            print("------------------GAME OVER--------------------")     
        elif monster_obiect.status == "edible":
            index_to_del = self.__active_monster.index(monster_obiect)
            del self.__active_monster[index_to_del]
            self.__Total_points += 100
    
    
    def PacMan_vs_Food(self,pacman_obiect:Sprites.PacMan, 
                          food_obiect:Sprites.Booster,
                          monster_set:list[Sprites.Monster]):
        if food_obiect.check_booster_effect == "SpeedUpPacman":
            food_obiect.SpeedUpPacman(pacman_obiect) 
        elif food_obiect.check_booster_effect == "SickMonster":
            food_obiect.SickMonster(monster_set=monster_set) 
        index_to_del = self.__active_food.index(food_obiect)
        del self.__active_food[index_to_del]
        
    def ColectCoin(self,coin_object):
        self.__Total_points += 1 
        index_to_del = self.__active_coins.index(coin_object)
        del self.__active_coins[index_to_del]
        
    def Print_Total_score(self):
        print(F"Total Score: {self.__Total_points}")
        
        
    @staticmethod
    def DoNothing():
        pass
        
    def Colitions_old(self,one_sprite, second_sprite):
        pacman_object, monster_object, food_object, coin_object = self.determine_which_pacman_monster_food(one_sprite,second_sprite)
        colition_dict = {("PacMan","Monster"):self.PacMan_vs_Monster(pacman_object,monster_object),
                         ("PacMan","Booster"):self.PacMan_vs_Food(pacman_object,
                                                                  food_object,
                                                                  self.__active_monster),
                         ("PacMan","Coin"):self.ColectCoin(),
                         ("Monster","PacMan"):self.PacMan_vs_Monster(pacman_object,
                                                                     monster_object),
                         ("Monster","Booster"):self.DoNothing(),
                         ("Monster","Coin"):self.DoNothing()}
        
        print("Class names: ", str(one_sprite.__class__.__name__), str(second_sprite.__class__.__name__))
        colition_dict[(str(one_sprite.__class__.__name__),
                                str(second_sprite.__class__.__name__))]
        
    
    def Colitions(self,one_sprite, second_sprite):
        pacman_object, monster_object, food_object, coin_object = self.determine_which_pacman_monster_food(one_sprite,second_sprite)
        class_names_tuple = (str(one_sprite.__class__.__name__),str(second_sprite.__class__.__name__))
        if class_names_tuple == ("PacMan","Monster") or class_names_tuple == ("Monster","PacMan"):
            self.PacMan_vs_Monster(pacman_object,monster_object)
        elif class_names_tuple == ("PacMan","Booster"):
            self.PacMan_vs_Food(pacman_object,food_object,self.__active_monster)
        elif class_names_tuple == ("PacMan","Coin"):
            self.ColectCoin(coin_object)
        elif class_names_tuple == ("Monster","Booster") or class_names_tuple == ("Monster","Coin"):
            self.DoNothing()
               
        
        
    def WhatIsHere(self,col,row):
        return self.__map[row][col] 
    
    def CanIMoveThere(self,x,y):
        print(f"CanIMoveThere: number of rows: {len(self.__map)}, number of columnes: {len(self.__map[1])}, x: {x}, y: {y}")
        if 0 <= x < len(self.__map[1]) and  0 <= y < len(self.__map):
            if self.__map[y][x].type == "Wall":
                return False
            else:
                return True
        else: 
            return False
    
    @property
    def DistanceToPacMan(self,x,y):
        distance = math.sqrt((self.__PacManPossition[0]-x)**2+(self.__PacManPossition[1]-y)**2)
        return distance
    
    
    
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
                        "Monster_sick":"./pic/normal_monster_sick.jpg",
                        "Path":"./pic/normal_path.jpg",
                        "Coin":"./pic/normal_coin.jpg"}
    
    def __init__(self,tile_string:str,board_mode="normal") -> None:
        self.type = ""
        self.pic = ""
        self.board_mode = board_mode
        
        self.type = self.TypeOfTiles[tile_string]
        if self.board_mode == "normal":
            self.pic = pygame.image.load(self.normal_pic_dict[self.type])
    
    def update_pic(self,new_type):
        # print(f"update_pic: {list(self.normal_pic_dict.keys())}")
        # old_type = list(self.normal_pic_dict.keys())[self.normal_pic_dict.values().index(self.type)]
        for key in self.normal_pic_dict:
            # print(f"update_pic: key: {key}, old type: {self.type}")
            if self.type == key:
                old_type = self.type
                # print(f"update_pic: old type: {old_type}, new: {new_type}")
                if old_type != new_type:
                    self.type = new_type
                    self.pic = pygame.image.load(self.normal_pic_dict[self.type])

 
        