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
                    
    screen_width = x_number_of_columns*20
    screen_height =  y_number_of_rows*20
    screen = pygame.display.set_mode([screen_width,screen_height])
    

    # Run until the user asks to quit
    running = True
    PacMan = Sprites.PacMan(0,0)
    Map = Board.Board(map_list=map_lines,Pacman=PacMan,screen=screen)
    game_state = "start_menu"

    loopcounter = 0
    while running:
        if game_state == "start_menu":
            screen.fill((0, 0, 0))
            font = pygame.font.SysFont('arial', 40)
            title = font.render('My Game - PacMan', True, (255, 255, 255))
            start_button = font.render('Start', True, (255, 255, 255))
            screen.blit(title, (screen_width/2 - title.get_width()/2, screen_height/2 - title.get_height()/2))
            screen.blit(start_button, (screen_width/2 - start_button.get_width()/2, screen_height/2 + start_button.get_height()/2))
            start_button_area = [[screen_width/2 - start_button.get_width()/2,screen_width/2 + start_button.get_width()/2],
                                [screen_height/2 - start_button.get_height()/2,screen_height/2 + start_button.get_height()/2]] 
            pygame.display.update()
            for ev in pygame.event.get():  
                if ev.type == pygame.QUIT:  
                pygame.quit()  
                if ev.type == pygame.MOUSEBUTTONDOWN:  
                      if start_button_area[0][0] <= mouse[0] <= start_button_area[0][1] and start_button_area[1][0] <= mouse[1] <= start_button_area[1][1]:  
                        pygame.quit()
                        game_state = "game"
  
        if game_state == "game":
            keys = pygame.key.get_pressed()
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
            game_state = Map.UpdateBoard(PacMan)
            Map.Print_Total_score()
                    
        if game_state == "the end":
            Map.DrawGameOver()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
         
    # Done! Time to quit.
    
    pygame.quit()
