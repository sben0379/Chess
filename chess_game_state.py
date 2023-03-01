"""This file contains the code necessary to keep track the state of the board at any given turn. The board is
represented # by a 2D list. Each piece is represented by a piece 'code' (eg. BQ = Black Queen), while '~~' stands for
an empty square. The rules for each piece are imported from the chess_pieces module and assigned as values to each
piece code. The get_piece() and make_move() methods can be called in the main function to modify the GameState list.
The rules for check, castling etc. will also be stored here."""

from chess_pieces import King, Queen, Rook, Bishop, Knight, Pawn


class GameState:
    def __init__(self):
        self.board = [
            ['BR', 'BN', 'BB', 'BQ', 'BK', 'BB', 'BN', 'BR'],
            ['BP', 'BP', 'BP', 'BP', 'BP', 'BP', 'BP', 'BP'],
            ['~~', '~~', '~~', '~~', '~~', '~~', '~~', '~~'],
            ['~~', '~~', '~~', '~~', '~~', '~~', '~~', '~~'],
            ['~~', '~~', '~~', '~~', '~~', '~~', '~~', '~~'],
            ['~~', '~~', '~~', '~~', '~~', '~~', '~~', '~~'],
            ['WP', 'WP', 'WP', 'WP', 'WP', 'WP', 'WP', 'WP'],
            ['WR', 'WN', 'WB', 'WQ', 'WK', 'WB', 'WN', 'WR']
        ]

        self.white_king = None
        self.black_king = None
        self.moves = []

    piece_classes = {
        'WK': King,
        'BK': King,
        'WQ': Queen,
        'BQ': Queen,
        'WR': Rook,
        'BR': Rook,
        'WB': Bishop,
        'BB': Bishop,
        'WN': Knight,
        'BN': Knight,
        'WP': Pawn,
        'BP': Pawn
    }

    # The future_board() method duplicates the current board as dictated by the GameState class. We can use it in order
    # to 'test out' moves in order to check that they are legal before making changes to the real board.
    def future_board(self):
        future_board = GameState()
        future_board.board = [row[:] for row in self.board]
        return future_board

    # The make_move() method alters the state of the board when called in the main function by swapping the element in
    # the target square with the element in the origin square, and then changing the origin square to an empty space.
    # However we will first check if either of the special castling or promotion moves have been played, as those will
    # require extra functionality beyond just swapping squares.
    def make_move(self, origin, destination):
        self.board[destination[0]][destination[1]] = self.board[origin[0]][origin[1]]
        self.board[origin[0]][origin[1]] = '~~'

    # Add the most recent move as a list of tuples to the self.moves list, creating a 2D list.
    def add_move(self, origin, destination):
        move = [origin, destination]
        self.moves.append(move)

    # Separate function for pawn moves to check for en passant and promotion

    def make_pawn_move(self, origin, destination):
        if self.board[origin[0]][origin[1]] == 'WP' and destination[0] == 0:
            self.board[destination[0]][destination[1]] = 'WQ'
            self.board[origin[0]][origin[1]] = '~~'
        elif self.board[origin[0]][origin[1]] == 'BP' and destination[0] == 7:
            self.board[destination[0]][destination[1]] = 'BQ'
            self.board[origin[0]][origin[1]] = '~~'
        else:
            self.board[destination[0]][destination[1]] = self.board[origin[0]][origin[1]]
            self.board[origin[0]][origin[1]] = '~~'

    # Separate function to make a king move to allow for castling:

    def make_king_move(self, origin, destination, colour):
        if colour == 'W':
            if destination == (7, 6) and origin == (7, 4):
                self.board[7][6] = 'WK'
                self.board[7][5] = 'WR'
                self.board[7][4] = '~~'
            elif destination == (7, 2) and origin == (7, 4):
                self.board[7][2] = 'WK'
                self.board[7][3] = 'WR'
                self.board[7][4] = '~~'
            else:
                self.board[destination[0]][destination[1]] = self.board[origin[0]][origin[1]]
                self.board[origin[0]][origin[1]] = '~~'
        elif colour == 'B':
            if destination == (0, 6) and origin == (0, 4):
                self.board[0][6] = 'BK'
                self.board[0][5] = 'BR'
                self.board[0][4] = '~~'
            elif destination == (0, 2) and origin == (0, 4):
                self.board[0][2] = 'BK'
                self.board[0][3] = 'BR'
                self.board[0][4] = '~~'
            else:
                self.board[destination[0]][destination[1]] = self.board[origin[0]][origin[1]]
                self.board[origin[0]][origin[1]] = '~~'

        # If a player attempts to castle, we must check if either the king or the rook on the side which the player is
        # trying to castle on has moved during the game. If either one has, castling would be illegal and we should
        # return False.

    def castle(self, colour, side):
        if colour == 'W':
            if side == 'Kingside':
                for move in self.moves:
                    if (7, 4) in move or (7, 7) in move:
                        return False
                return True
            elif side == 'Queenside':
                for move in self.moves:
                    if (7, 4) in move or (7, 0) in move:
                        return False
                return True
        elif colour == 'B':
            if side == 'Kingside':
                for move in self.moves:
                    if (0, 4) in move or (0, 7) in move:
                        return False
                return True
            elif side == 'Queenside':
                for move in self.moves:
                    if (0, 4) in move or (0, 0) in move:
                        return False
                return True

    # The get_piece() method accesses the piece_classes dictionary and returns the piece present at any given square.
    def get_piece(self, row, col):
        piece = self.board[row][col]
        if piece == '~~':
            return None
        return self.piece_classes[piece]

    # The check_turn() method takes the piece selected and whose turn it is according to main as arguments and returns
    # True if they match.
    def check_turn(self, colour, origin):
        if colour == self.board[origin[0]][origin[1]][0]:
            return True
        else:
            return False

    def in_check(self, colour):
        # Find the positions of the kings
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if self.board[row][col] == 'WK':
                    self.white_king = (row, col)
                elif self.board[row][col] == 'BK':
                    self.black_king = (row, col)

        if colour == 'W':
            # Check if any black piece can attack the white king
            for row in range(len(self.board)):
                for col in range(len(self.board[row])):
                    piece = self.board[row][col]
                    if piece[0] == 'B' and piece != 'BK':
                        piece_square = (row, col)
                        attacking_piece = self.piece_classes[piece](piece_square, self.white_king, self.board)
                        if attacking_piece.check_move():
                            return True
            return False
        elif colour == 'B':
            # Check if any white piece can attack the black king
            for row in range(len(self.board)):
                for col in range(len(self.board[row])):
                    piece = self.board[row][col]
                    if piece[0] == 'W' and piece != 'WK':
                        piece_square = (row, col)
                        attacking_piece = self.piece_classes[piece](piece_square, self.black_king, self.board)
                        if attacking_piece.check_move():
                            return True
            return False

