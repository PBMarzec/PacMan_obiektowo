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
    PacMan = Sprites.PacMan(0,0)
    Map = Board.Board(map_list=map_lines,Pacman=PacMan,screen=screen)
    Map.DrowBoard()

    loopcounter = 0
    while running:
        Map.DrowBoard()    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                Map.Print_Total_score()
            elif event.type == pygame.KEYDOWN:
                pressed_keys = pygame.key.get_pressed()
                if event.key == pygame.K_ESCAPE:
                    running = False
                    Map.Print_Total_score()
                if event.key == pygame.K_UP:
                    PacMan.move([0,-1],Map)
                if event.key == pygame.K_DOWN:
                    PacMan.move([0, 1],Map)
                if event.key == pygame.K_LEFT:
                    PacMan.move([-1, 0],Map)
                if event.key == pygame.K_RIGHT:
                    PacMan.move([1, 0],Map)
                    
        if loopcounter == 10:
            for monster in Map.active_monster:
                monster.move(Sprites.Monster.MoveStrategy(self=monster,board=Map),Map)
            loopcounter = 0
        else:
            loopcounter += 1
        Map.UpdateBoard(PacMan)
        Map.Print_Total_score()
        
         
    # Done! Time to quit.
    Map.Print_Total_score()
    pygame.quit()
