import pygame

# To start drawing out the board, we will specify the size of the board and the squares. We will also create a
# dictionary to map each piece code to the corresponding image.

width = height = 512
sq_size = height // 8
images = {}
white_pieces = ['WP', 'WN', 'WB', 'WR', 'WQ', 'WK']
black_pieces = ['BP', 'BN', 'BB', 'BR', 'BQ', 'BK']


# Define load images function to loop through list of pieces and set the value to each piece key in the dictionary to
# the corresponding image.

def load_images():
    pieces = white_pieces + black_pieces
    for piece in pieces:
        images[piece] = pygame.transform.scale(pygame.image.load('/Users/james/Desktop/Python Projects/Chess/Images/' +
                                                                 piece + '.png'), (sq_size, sq_size))


# Create a class GameState that will keep track of the board and position of the pieces at all times. The board is in
# the form of an 8x8 2D list where each piece is represented by a code and empty squares are represented by ##. The
# starting position can thus be represented as follows.

class GameState:
    def __init__(self):
        self.board = [
            ['BR', 'BN', 'BB', 'BQ', 'BK', 'BB', 'BN', 'BR'],
            ['BP', 'BP', 'BP', 'BP', 'BP', 'BP', 'BP', 'BP'],
            ['##', '##', '##', '##', '##', '##', '##', '##'],
            ['##', '##', '##', '##', '##', '##', '##', '##'],
            ['##', '##', '##', '##', '##', '##', '##', '##'],
            ['##', '##', '##', '##', '##', '##', '##', '##'],
            ['WP', 'WP', 'WP', 'WP', 'WP', 'WP', 'WP', 'WP'],
            ['WR', 'WN', 'WB', 'WQ', 'WK', 'WB', 'WN', 'WR']
        ]

    def make_move(self, move):
        self.board[move.end_row][move.end_col] = move.origin  # Swap second square with first square
        self.board[move.start_row][move.start_col] = '##'  # Swap first square with empty square
        pygame.display.update()


# Create Move class to hold move behaviours
class Move:
    def __init__(self, start, end, board):
        self.start_row = start[0]
        self.start_col = start[1]
        self.end_row = end[0]
        self.end_col = end[1]
        self.origin = board[self.start_row][self.start_col]
        self.destination = board[self.end_row][self.end_col]


# Create the pawn class to define the legal moves of a pawn. It can move one square forward (unless on the start row, in
# which case is may move two) and captures diagonally. If there is a piece in front of it, it may not move. Pass in the
# requested move from the user and if it satisfies the conditions, return True. Else, return false.
class Pawn:
    def __init__(self, start, end, board):
        self.start_row = start[0]
        self.start_col = start[1]
        self.end_row = end[0]
        self.end_col = end[1]
        self.origin = board[self.start_row][self.start_col]
        self.destination = board[self.end_row][self.end_col]
        self.in_between = board[self.end_row - 1][self.end_col]

    def check_move(self):
        if self.origin == 'WP':  # White pawns move 'up' the board, but backwards in the 2D list
            if self.start_row == 6:  # If pawn is on starting row then we must also allow for double forward moves
                if self.end_row == 4 and self.start_col == self.end_col and self.destination == '##' and \
                        self.in_between == '##':
                    return True  # If pawn is on starting row then may move forward twice if no piece in between
                elif self.end_row == 5 and self.start_col == self.end_col and self.destination == '##':
                    return True  # Move one square up if it is unoccupied
                elif self.end_row == 5 and self.start_col - self.end_col == -1 and self.destination == 'BP' or \
                        self.destination == 'BN' or self.destination == 'BB' or self.destination == 'BR' or \
                        self.destination == 'BQ':
                    return True  # Move one square up and to the right if square is occupied by an enemy piece
                elif self.end_row == 5 and self.start_col - self.end_col == 1 and self.destination == 'BP' or \
                        self.destination == 'BN' or self.destination == 'BB' or self.destination == 'BR' or \
                        self.destination == 'BQ':
                    return True  # Move one square up and to the left if square is occupied by an enemy piece
                else:
                    return False
            else:  # Same rules for all other starting squares minus ability to move twice
                if self.start_row - self.end_row == 1 and self.start_col == self.end_col and self.destination == '##':
                    return True
                elif self.start_row - self.end_row == 1 and self.start_col - self.end_col == -1 and self.destination \
                        == 'BP' or self.destination == 'BN' or self.destination == 'BB' or self.destination == 'BR' or \
                        self.destination == 'BQ':
                    return True
                elif self.start_row - self.end_row == 1 and self.start_col - self.end_col == 1 and self.destination \
                        == 'BP' or self.destination == 'BN' or self.destination == 'BB' or self.destination == 'BR' or \
                        self.destination == 'BQ':
                    return True
                else:
                    return False
        elif self.origin == 'BP':  # Same rules for black pawns but in reverse
            if self.start_row == 1:
                if self.end_row == 3 and self.start_col == self.end_col and self.destination == '##' and \
                        self.in_between == '##':
                    return True
                elif self.end_row == 2 and self.start_col == self.end_col and self.destination == '##':
                    return True
                elif self.end_row == 2 and self.start_col - self.end_col == -1 and self.destination == 'WP' or \
                        self.destination == 'WN' or self.destination == 'WB' or self.destination == 'WR' or \
                        self.destination == 'WQ':
                    return True
                elif self.end_row == 2 and self.start_col - self.end_col == 1 and self.destination == 'WP' or \
                        self.destination == 'WN' or self.destination == 'WB' or self.destination == 'WR' or \
                        self.destination == 'WQ':
                    return True
                else:
                    return False
            else:
                if self.start_row - self.end_row == -1 and self.start_col == self.end_col and self.destination == '##':
                    return True
                elif self.start_row - self.end_row == -1 and self.start_col - self.end_col == -1 and self.destination \
                        == 'WP' or self.destination == 'WN' or self.destination == 'WB' or self.destination == 'WR' or \
                        self.destination == 'WQ':
                    return True
                elif self.start_row - self.end_row == -1 and self.start_col - self.end_col == 1 and self.destination \
                        == 'WP' or self.destination == 'WN' or self.destination == 'WB' or self.destination == 'WR' or \
                        self.destination == 'WQ':
                    return True
                else:
                    return False


# Create the knight class to define the legal moves of a knight. It may move one square vertically and two squares
# vertically, or vice versa, unless the destination square is occupied by a friendly piece.

class Knight:
    def __init__(self, start, end, board):
        self.start_row = start[0]
        self.start_col = start[1]
        self.end_row = end[0]
        self.end_col = end[1]
        self.origin = board[self.start_row][self.start_col]
        self.destination = board[self.end_row][self.end_col]

    def check_move(self):
        if (self.origin == 'WN' and self.destination not in white_pieces) or (self.origin == 'BN' and self.destination
                                                                              not in black_pieces):
            if (self.end_row - self.start_row == 2 and self.end_col - self.start_col == -1) or (
                    self.end_row - self.start_row == 1 and self.end_col - self.start_col == -2) or (
                    self.end_row - self.start_row == -1 and self.end_col - self.start_col == -2) or (
                    self.end_row - self.start_row == -2 and self.end_col - self.start_col == -1) or (
                    self.end_row - self.start_row == -2 and self.end_col - self.start_col == 1) or (
                    self.end_row - self.start_row == -1 and self.end_col - self.start_col == 2) or (
                    self.end_row - self.start_row == 1 and self.end_col - self.start_col == 2) or (
                    self.end_row - self.start_row == 2 and self.end_col - self.start_col == 1):
                return True
            else:
                return False


# Create the bishop class to define the legal moves of a bishop. A bishop may move diagonally in any direction until it
# meets another piece or reaches the end of the board. If that piece is a friendly piece, it must stop one square
# before. If it is an enemy piece, the bishop may take its place.

class Bishop:
    def __init__(self, start, end, board):
        self.start_row = start[0]
        self.start_col = start[1]
        self.end_row = end[0]
        self.end_col = end[1]
        self.board = board
        self.origin = board[self.start_row][self.start_col]
        self.destination = board[self.end_row][self.end_col]

    def check_move(self):
        if (self.origin == 'WB' and self.destination not in white_pieces) or (self.origin == 'BB' and self.destination
                                                                              not in black_pieces):
            if self.end_row < self.start_row and self.end_col < self.start_col:  # Check northwest
                r, c = self.start_row - 1, self.start_col - 1
                while r > -1 and c > -1:
                    if self.board[r][c] == self.destination:
                        return True
                    elif self.board[r][c] == '##':
                        r -= 1
                        c -= 1
                        continue  # Carry on checking squares if we come across an empty square
                    else:
                        return False  # If square is not empty or the target square then the path must be blocked
                return False
            elif self.end_row > self.start_row and self.end_col < self.start_col:  # Check southwest
                r, c = self.start_row + 1, self.start_col - 1
                while r < 8 and c > -1:
                    if self.board[r][c] == self.destination:
                        return True
                    elif self.board[r][c] == '##':
                        r += 1
                        c -= 1
                        continue
                    else:
                        return False
                return False
            elif self.end_row > self.start_row and self.end_col > self.start_col:  # Check southeast
                r, c = self.start_row + 1, self.start_col + 1
                while r < 8 and c < 8:
                    if self.board[r][c] == self.destination:
                        return True
                    elif self.board[r][c] == '##':
                        r += 1
                        c += 1
                        continue
                    else:
                        return False
                return False
            elif self.end_row < self.start_row and self.end_col > self.start_col:  # Check northeast
                r, c = self.start_row - 1, self.start_col + 1
                while r > -1 and c < 8:
                    if self.board[r][c] == self.destination:
                        return True
                    elif self.board[r][c] == '##':
                        r -= 1
                        c += 1
                        continue
                    else:
                        return False
                return False


# Create the rook class to define the legal moves of a rook. The rook may move in a straight line in any direction until
# it meets another piece of the edge of the board. If that piece is a friendly piece, it must stop one square before. If
# it is an enemy piece, the rook may take its place.

class Rook:
    def __init__(self, start, end, board):
        self.start_row = start[0]
        self.start_col = start[1]
        self.end_row = end[0]
        self.end_col = end[1]
        self.board = board
        self.origin = board[self.start_row][self.start_col]
        self.destination = board[self.end_row][self.end_col]

    def check_move(self):
        if (self.origin == 'WR' and self.destination not in white_pieces) or (self.origin == 'BR' and self.destination
                                                                              not in black_pieces):
            if self.end_row < self.start_row and self.end_col == self.start_col:  # Check north
                r, c = self.start_row - 1, self.start_col
                while r > -1:
                    if self.board[r][c] == self.destination:
                        return True
                    elif self.board[r][c] == '##':
                        r -= 1
                        continue  # Carry on checking if we come across empty square
                    else:
                        return False  # If square is not empty or the target square then the path must be blocked
                return False
            elif self.end_row == self.start_row and self.end_col < self.start_col:  # Check west
                r, c = self.start_row, self.start_col - 1
                while c > -1:
                    if self.board[r][c] == self.destination:
                        return True
                    elif self.board[r][c] == '##':
                        c -= 1
                        continue
                    else:
                        return False
                return False
            elif self.end_row > self.start_row and self.end_col == self.start_col:  # Check south
                r, c = self.start_row + 1, self.start_col
                while r < 8:
                    if self.board[r][c] == self.destination:
                        return True
                    elif self.board[r][c] == '##':
                        r += 1
                        continue
                    else:
                        return False
                return False
            elif self.end_row == self.start_row and self.end_col > self.start_col:  # Check east
                r, c = self.start_row, self.start_col + 1
                while c < 8:
                    if self.board[r][c] == self.destination:
                        return True
                    elif self.board[r][c] == '##':
                        c += 1
                        continue
                    else:
                        return False
                return False


# Create the queen class to define the legal moves of a queen. The queen may move in any direction until it meets
# another piece of the edge of the board. If that piece is a friendly piece, it must stop one square before. If it is
# an enemy piece, the queen may take its place.

class Queen:
    def __init__(self, start, end, board):
        self.start_row = start[0]
        self.start_col = start[1]
        self.end_row = end[0]
        self.end_col = end[1]
        self.board = board
        self.origin = board[self.start_row][self.start_col]
        self.destination = board[self.end_row][self.end_col]

    def check_move(self):
        if (self.origin == 'WQ' and self.destination not in white_pieces) or (self.origin == 'BQ' and self.destination
                                                                              not in black_pieces):
            if self.end_row < self.start_row and self.end_col == self.start_col:  # Check north
                r, c = self.start_row - 1, self.start_col
                while r > -1:
                    if self.board[r][c] == self.destination:
                        return True
                    elif self.board[r][c] == '##':
                        r -= 1
                        continue  # Carry on checking if we come across empty square
                    else:
                        return False  # If square is not empty or the target square then the path must be blocked
                return False
            elif self.end_row == self.start_row and self.end_col < self.start_col:  # Check west
                r, c = self.start_row, self.start_col - 1
                while c > -1:
                    if self.board[r][c] == self.destination:
                        return True
                    elif self.board[r][c] == '##':
                        c -= 1
                        continue
                    else:
                        return False
                return False
            elif self.end_row > self.start_row and self.end_col == self.start_col:  # Check south
                r, c = self.start_row + 1, self.start_col
                while r < 8:
                    if self.board[r][c] == self.destination:
                        return True
                    elif self.board[r][c] == '##':
                        r += 1
                        continue
                    else:
                        return False
                return False
            elif self.end_row == self.start_row and self.end_col > self.start_col:  # Check east
                r, c = self.start_row, self.start_col + 1
                while c < 8:
                    if self.board[r][c] == self.destination:
                        return True
                    elif self.board[r][c] == '##':
                        c += 1
                        continue
                    else:
                        return False
            elif self.end_row < self.start_row and self.end_col < self.start_col:  # Check northwest
                r, c = self.start_row - 1, self.start_col - 1
                while r > -1 and c > -1:
                    if self.board[r][c] == self.destination:
                        return True
                    elif self.board[r][c] == '##':
                        r -= 1
                        c -= 1
                        continue
                    else:
                        return False
                return False
            elif self.end_row > self.start_row and self.end_col < self.start_col:  # Check southwest
                r, c = self.start_row + 1, self.start_col - 1
                while r < 8 and c > -1:
                    if self.board[r][c] == self.destination:
                        return True
                    elif self.board[r][c] == '##':
                        r += 1
                        c -= 1
                        continue
                    else:
                        return False
                return False
            elif self.end_row > self.start_row and self.end_col > self.start_col:  # Check southeast
                r, c = self.start_row + 1, self.start_col + 1
                while r < 8 and c < 8:
                    if self.board[r][c] == self.destination:
                        return True
                    elif self.board[r][c] == '##':
                        r += 1
                        c += 1
                        continue
                    else:
                        return False
                return False
            elif self.end_row < self.start_row and self.end_col > self.start_col:  # Check northeast
                r, c = self.start_row - 1, self.start_col + 1
                while r > -1 and c < 8:
                    if self.board[r][c] == self.destination:
                        return True
                    elif self.board[r][c] == '##':
                        r -= 1
                        c += 1
                        continue
                    else:
                        return False
            return False


# Create the king class to define the legal moves of a king. The king may move in any direction by one square, provided
# that it is not occupied by a friendly piece. Check compass points as before.

class King:
    def __init__(self, start, end, board):
        self.start_row = start[0]
        self.start_col = start[1]
        self.end_row = end[0]
        self.end_col = end[1]
        self.board = board
        self.origin = board[self.start_row][self.start_col]
        self.destination = board[self.end_row][self.end_col]

    def check_move(self):
        if (self.origin == 'WK' and self.destination not in white_pieces) or (self.origin == 'BK' and self.destination
                                                                              not in black_pieces):
            if (self.end_row - self.start_row == -1 and self.end_col - self.start_col == 0) or (
                    self.end_row - self.start_row == -1 and self.end_col - self.start_col == 1) or (
                    self.end_row - self.start_row == 0 and self.end_col - self.start_col == 1) or (
                    self.end_row - self.start_row == 1 and self.end_col - self.start_col == 1) or (
                    self.end_row - self.start_row == 1 and self.end_col - self.start_col == 0) or (
                    self.end_row - self.start_row == 1 and self.end_col - self.start_col == -1) or (
                    self.end_row - self.start_row == 0 and self.end_col - self.start_col == -1) or (
                    self.end_row - self.start_row == -1 and self.end_col - self.start_col == -1):
                return True
            else:
                return False

# Define main function to act as our driver for the game. We'll start by setting up the screen and importing the game
# state from our chess engine file.

def main():
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    gs = GameState()  # gs is now an instance of the game
    load_images()
    sq_clicked = ()  # xy coordinates of the square clicked
    move_queue = []  # Keeps track of last two clicks to determine the move intended
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:  # Getting user mouse input
                x, y = pygame.mouse.get_pos()
                row = y // sq_size
                col = x // sq_size
                sq_clicked = (row, col)
                move_queue.append(sq_clicked)
                if len(move_queue) == 2:  # Call move function after second click
                    if gs.board[move_queue[0][0]][move_queue[0][1]] == 'WP' or \
                            gs.board[move_queue[0][0]][move_queue[0][1]] == 'BP':
                        piece_selected = Pawn(move_queue[0], move_queue[1], gs.board)
                        if piece_selected.check_move():
                            move = Move(move_queue[0], move_queue[1], gs.board)
                            gs.make_move(move)
                            sq_clicked = ()  # Reset variables so they can be used for the next move
                            move_queue = []
                        else:
                            sq_clicked = ()
                            move_queue = []
                    elif gs.board[move_queue[0][0]][move_queue[0][1]] == 'WN' or \
                            gs.board[move_queue[0][0]][move_queue[0][1]] == 'BN':
                        piece_selected = Knight(move_queue[0], move_queue[1], gs.board)
                        if piece_selected.check_move():
                            move = Move(move_queue[0], move_queue[1], gs.board)
                            gs.make_move(move)
                            sq_clicked = ()  # Reset variables so they can be used for the next move
                            move_queue = []
                        else:
                            sq_clicked = ()
                            move_queue = []
                    elif gs.board[move_queue[0][0]][move_queue[0][1]] == 'WB' or \
                            gs.board[move_queue[0][0]][move_queue[0][1]] == 'BB':
                        piece_selected = Bishop(move_queue[0], move_queue[1], gs.board)
                        if piece_selected.check_move():
                            move = Move(move_queue[0], move_queue[1], gs.board)
                            gs.make_move(move)
                            sq_clicked = ()  # Reset variables so they can be used for the next move
                            move_queue = []
                        else:
                            sq_clicked = ()
                            move_queue = []
                    elif gs.board[move_queue[0][0]][move_queue[0][1]] == 'WR' or \
                            gs.board[move_queue[0][0]][move_queue[0][1]] == 'BR':
                        piece_selected = Rook(move_queue[0], move_queue[1], gs.board)
                        if piece_selected.check_move():
                            move = Move(move_queue[0], move_queue[1], gs.board)
                            gs.make_move(move)
                            sq_clicked = ()  # Reset variables so they can be used for the next move
                            move_queue = []
                        else:
                            sq_clicked = ()
                            move_queue = []
                    elif gs.board[move_queue[0][0]][move_queue[0][1]] == 'WQ' or \
                            gs.board[move_queue[0][0]][move_queue[0][1]] == 'BQ':
                        piece_selected = Queen(move_queue[0], move_queue[1], gs.board)
                        if piece_selected.check_move():
                            move = Move(move_queue[0], move_queue[1], gs.board)
                            gs.make_move(move)
                            sq_clicked = ()  # Reset variables so they can be used for the next move
                            move_queue = []
                        else:
                            sq_clicked = ()
                            move_queue = []
                    elif gs.board[move_queue[0][0]][move_queue[0][1]] == 'WK' or \
                            gs.board[move_queue[0][0]][move_queue[0][1]] == 'BK':
                        piece_selected = King(move_queue[0], move_queue[1], gs.board)
                        if piece_selected.check_move():
                            move = Move(move_queue[0], move_queue[1], gs.board)
                            gs.make_move(move)
                            sq_clicked = ()  # Reset variables so they can be used for the next move
                            move_queue = []
                        else:
                            sq_clicked = ()
                            move_queue = []
        render_game_state(screen, gs)
    pygame.quit()


# Define render board function to alternate colours from squares to square. If we assign each row and each column a
# number 0-8, we can alternate colours with a nested loop by checking whether a square is even or odd.

def render_board(screen):
    for row in range(8):
        for col in range(8):
            if row % 2 == 0 and col % 2 == 0:
                color = pygame.Color('white')
                pygame.draw.rect(screen, color, pygame.Rect(row * sq_size, col * sq_size, sq_size, sq_size))
            elif row % 2 != 0 and col % 2 == 0:
                color = pygame.Color('dark green')
                pygame.draw.rect(screen, color, pygame.Rect(row * sq_size, col * sq_size, sq_size, sq_size))
            elif row % 2 == 0 and col % 2 != 0:
                color = pygame.Color('dark green')
                pygame.draw.rect(screen, color, pygame.Rect(row * sq_size, col * sq_size, sq_size, sq_size))
            else:
                color = pygame.Color('white')
                pygame.draw.rect(screen, color, pygame.Rect(row * sq_size, col * sq_size, sq_size, sq_size))


# Define render pieces function to use a nested loop in order to blit piece images on to the board according to the
# piece codes we specified in our GameState class.

def render_pieces(screen, board):
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece != '##':
                screen.blit(images[piece], pygame.Rect(col * sq_size, row * sq_size, sq_size, sq_size))


# Define render game state function that will graphically represent the render board and pieces functions relative to
# the current state of the game.

def render_game_state(screen, gs):
    render_board(screen)
    render_pieces(screen, gs.board)
    pygame.display.update()


main()
