import pygame
from copy import deepcopy
import Board
import Sprites




if __name__ == "__main__":
    
    boardfile="board_1.txt"
    pygame.init()

    # Set up the drawing window
    with open(boardfile, 'r') as mapfile:
            map_lines = mapfile.readlines()
            y_number_of_rows = len(map_lines)
            x_number_of_columns = len(map_lines[0])-1
                    
    screen = pygame.display.set_mode([x_number_of_columns*20, y_number_of_rows*20])
    

    # Run until the user asks to quit
    running = True
    PacMan = Sprites.PacMan
    Map = Board.Board(map_list=map_lines,Pacman=PacMan,screen=screen)
    Map.DrowBoard()

    loopcounter = 0
    while running:
        Map.DrowBoard()    
        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                pressed_keys = pygame.key.get_pressed()
                PacMan.move_pacman(PacMan,pressed_keys=pressed_keys)
        
        if loopcounter == 10:
            for monster in Map.active_monster:
                monster.move(Sprites.Monster.MoveStrategy(self=monster,board=Map),Map)
            loopcounter = 0
        else:
            loopcounter += 1
        
        Map.UpdateBoard(PacMan)
        
         
    # Done! Time to quit.
    pygame.quit()
