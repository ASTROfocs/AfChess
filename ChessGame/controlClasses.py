# Imports
import pygame as pg

from constsAndTypes import *
from piecesClasses import *
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


# Classes
class Cursor:
    def __init__(self, position: Coord, board: 'ChessBoard'):
        self.position: Coord = position
        self.board = board
        
        # Using to move pieces. Maybe change None to empty piece?
        self.inside: Piece | None = None
    
    def move(self, direction: int):
        x, y = self.position
        if direction == UP and coord_valid((x, y - 1)):
            self.position = (x, y - 1)
        elif direction == RIGHT and coord_valid((x + 1, y)):
            self.position = (x + 1, y)
        elif direction == DOWN and coord_valid((x, y + 1)):
            self.position = (x, y + 1)
        elif direction == LEFT and coord_valid((x - 1, y)):
            self.position = (x - 1, y)
    
    def pick_up(self):
        print("pickup")
        self.inside = self.board.get_square(self.position)
    def put_down(self):
        print("put down")
        self.board.make_move()


class ChessBoard:
    def __init__(self) -> None:
        # pieces holds the pieces, board_state is built
        # through it and holds their positions as well

        # Wait maybe I can remove the piece list altogether
        self.board_state: dict[Coord, Piece] = {}
        self.cursor = Cursor((4, 4), self)
        self.pieces: list[Piece] = []

    def fill_pieces(self):
        for i in range(8):
            self.pieces.append(Pawn((i, 6), WHITE, self))
            self.pieces.append(Pawn((i, 1), BLACK, self))
            if i == 0:
                self.pieces.append(Rook((i,7), WHITE, self))
                self.pieces.append(Rook((i,0), BLACK, self))
            if i == 7:
                self.pieces.append(Rook((i,7), WHITE, self))
                self.pieces.append(Rook((i,0), BLACK, self))


    def update_board(self):
        self.board_state = {}
        for piece in self.pieces:
            self.board_state[piece.position] = piece

    # This method is superfluous, but might help with readability
    def get_square(self, coord: Coord):
        x, y = coord
        return self.board_state.get((x, y), None) 

    def recalc_pieces(self):
        for obj in self.board_state.values():
            # calculate method is common to all pieces
            obj.calculate()

    # How do I type the screen?    
    def render_bg(self, screen):
        color = 0
        offset_x = 0
        offset_y = 0
        for row in range(8):
            for square in range(8):
                board_square = pg.Rect((80*offset_x, 80*offset_y), SQUARE_SIZE)

                if color == 0:
                    pg.draw.rect(screen, 'White', board_square)
                    color = 1
                else:
                    pg.draw.rect(screen, 'Black', board_square)
                    color = 0

                offset_x += 1
            
            # offset reset after each row
            offset_x = 0
            offset_y += 1
            
            # so squares are checkered
            if offset_y % 2 == 0:
                color = 0
            else:
                color = 1

    def render_obj(self, screen):
        for obj in self.pieces:
            x, y = obj.position
            screen.blit(obj.image, (80*x, 80*y))

        x, y = self.cursor.position
        cursor_img = pg.Rect((x*80, y*80), SQUARE_SIZE)
        pg.draw.rect(screen, 'BLUE', cursor_img, 10)

    def render(self, screen):
        self.render_bg(screen)
        self.render_obj(screen)
    
    def make_move(self):
           # So capturing deletes a piece, else they stack 
           if self.cursor.position in self.board_state:
               self.pieces.remove(self.board_state[self.cursor.position])
           self.cursor.inside.position = self.cursor.position
           self.cursor.inside.moved = True # For pawn and king logic
           self.cursor.inside = None
        
# ---------
