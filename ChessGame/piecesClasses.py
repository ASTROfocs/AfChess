# Imports
import pygame as pg

from constsAndTypes import *
# -------

pg.init()


# Vars
screen = pg.display.set_mode((1240, 720))
test_font = pg.font.Font(None, 40)
white_turn = 1
# --------

# Functions
def coord_valid(coord: Coord):
    x, y = coord
    if 0 <= x < 8 and 0 <= y < 8:
        return True
    else:
        return False


class Pawn:
    def __init__(self, position: Coord, side: int, board: 'ChessBoard') -> None:
        self.position = position
        self.side = side
        self.board = board
        self.poss_moves: set[Coord] = set()
        self.name = 'WP' if self.side == WHITE else 'BP'
        self.image = test_font.render(f'{self.name}', True, 'Green')
        self.moved = False

    # Refactor this later
    #NOTE:This method leads to invalid coords being in poss_moves,
    # but that is okay since movement is done through cursor and he can't get there
    def moves(self):
        x, y = self.position
        if self.side == WHITE:
            if (x, y - 1) not in self.board.board_state.keys():
                self.poss_moves.add((x, y - 1))
            
            if not self.moved and (x, y - 2) not in self.board.board_state:
                self.poss_moves.add((x, y - 2))

            front_left = self.board.board_state.get((x - 1, y - 1))
            front_right = self.board.board_state.get((x + 1, y - 1))

            if front_right is not None and front_right.side == BLACK:
                self.poss_moves.add((x + 1, y - 1))
            if front_left is not None and front_left.side == BLACK:
                self.poss_moves.add((x - 1, y - 1))

        elif self.side == BLACK:
            if (x, y + 1) not in self.board.board_state.keys():
                self.poss_moves.add((x, y + 1))
            
            if not self.moved and (x, y + 2) not in self.board.board_state:
                self.poss_moves.add((x, y + 2))

            front_left = self.board.board_state.get((x - 1, y + 1))
            front_right = self.board.board_state.get((x + 1, y + 1))

            if front_right is not None and front_right.side == WHITE:
                self.poss_moves.add((x + 1, y + 1))
            if front_left is not None and front_left.side == WHITE:
                self.poss_moves.add((x - 1, y + 1))

    def calculate(self):
        # Do note that poss_moves must be reset
        self.poss_moves = set()
        self.moves()

class Rook:
    def __init__(self, position: Coord, side: int, board: 'ChessBoard') -> None:
        self.position = position
        self.side = side
        self.board = board
        self.poss_moves: set[Coord] = set()
        self.name = 'WR' if self.side == WHITE else 'BR'
        self.image = test_font.render(f'{self.name}', True, 'Green')
        self.moved = False

    def moves(self):
        x, y = self.position
        # Okay so simply create a bunch of tuples in each direction with an offset var
        # each turn, simply increment the offset. once coords not valid or the direction
        # gets messed up simply end it
        left = True
        right = True
        down = True
        up = True
        for row in range(1,8):
            # add logic for taking pieces
            if (x + row, y) not in self.board.board_state and right:
                self.poss_moves.add((x + row, y))
            else:
                right = False
            
            if (x - row, y) not in self.board.board_state and left:
                self.poss_moves.add((x - row, y))
            else:
                left = False

            if (x, y + row) not in self.board.board_state and down:
                self.poss_moves.add((x, y + row))
            else:
                down = False
            
            if (x, y - row) not in self.board.board_state and up:
                self.poss_moves.add((x, y - row))
            else:
                up = False

        

    def calculate(self):
        # Do note that poss_moves must be reset
        self.poss_moves = set()
        self.moves()
