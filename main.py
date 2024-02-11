import pygame
from copy import deepcopy
import Board
import Sprites




if __name__ == "__main__":
    pygame.init()

    # Set up the drawing window
    # screen = pygame.display.set_mode([500, 500])

    # Run until the user asks to quit
    running = True
    PacMan = Sprites.PacMan
    Map = Board.Board(boardfile="board_1.txt",Pacman=PacMan)
    Map.DrowBoard()

    loopcounter = 0
    while running:

        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pressed_keys = pygame.key.get_pressed()
        PacMan.move_pacman(pressed_keys=pressed_keys)
        
        if loopcounter == 10:
            for monster in Board.Board.monster_list:
                monster.move(Sprites.Monster.MoveStrategy(self=monster,board=Map))
            loopcounter = 0
        else:
            loopcounter += 1
        
        Map.UpdateBoard()
        Map.DrowBoard()    
         
    # Done! Time to quit.
    pygame.quit()
