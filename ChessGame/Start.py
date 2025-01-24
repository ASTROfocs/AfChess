# Imports
import pygame as pg
from sys import exit

from constsAndTypes import *
from controlClasses import *
from piecesClasses import *
# -------

pg.init()

# Functions
def coord_valid(coord: Coord):
    x, y = coord
    if 0 <= x < 8 and 0 <= y < 8:
        return True
    else:
        return False


board = ChessBoard()
board.fill_pieces()
board.update_board()

# There will be tons of recalculation here
# Maybe put a separate condition into running
# so that it only checks when state changes.
# We can do that since it's turn based.
while RUNNING:
    # Events
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        
        # Potential inconsistency here. Maybe we do not need to make moves through the board, just the cursor.
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                cursor_pos = board.get_square(board.cursor.position)
                if cursor_pos is not None:
                    board.cursor.pick_up()
            if event.key == pg.K_LSHIFT:
                # Okay so these are the conditions for the put down to work
                # will have to refactor this later.
                # a) something has to be inside cursor b) cannot put it on the same square
                # c) the move can be done according to rules of play
                if (board.cursor.inside is not None
                    and (board.cursor.position != board.cursor.inside.position) 
                    and (board.cursor.position in board.cursor.inside.poss_moves)):
                    board.cursor.put_down()

            if event.key == pg.K_w:
                board.cursor.move(UP)
            if event.key == pg.K_a:
                board.cursor.move(LEFT)
            if event.key == pg.K_s:
                board.cursor.move(DOWN)
            if event.key == pg.K_d:
                board.cursor.move(RIGHT)
    
    # ------
    board.update_board()
    screen.fill('Red')
    board.recalc_pieces()
    board.render(screen)
    pg.display.update() # HAS TO BE AT THE END
