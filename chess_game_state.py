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

    # The make_move() method alters the state of the board when called in the main function by swapping the element in
    # the target square with the element in the origin square, and then changing the origin square to an empty space.
    def make_move(self, origin, destination):
        self.board[destination[0]][destination[1]] = self.board[origin[0]][origin[1]]
        self.board[origin[0]][origin[1]] = '~~'

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

    def in_check(self, king):
        pass
        # Find the location of the king
        # Assess if any enemy piece can legally reach that square
        # Return False if not
