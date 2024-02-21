
class OneTile_copy:
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
    def __init__(self,pic_path:str) -> None:
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
                