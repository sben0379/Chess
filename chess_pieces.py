"""This file contains the classes that define each chess piece limit their movements according to the rules of chess.
For each piece, we pass in the two squares the user has clicked on and the current state of the board.
The first square clicked on (self.start_row + self.start_col -> self.origin) will be the piece selected and the second
(self.end_row + self.end_col -> self.destination) will be the target square. These are both relative to the board state
(self.board) when the move is played. The check_move() methods for each evaluate whether the move being requested by the
player is legal for the given piece."""

# Each of these piece 'codes' stand for one of the six piece types and are used to keep track of positions on the
# board in the GameState module

white_pieces = ['WP', 'WN', 'WB', 'WR', 'WQ', 'WK']
black_pieces = ['BP', 'BN', 'BB', 'BR', 'BQ', 'BK']


class Pawn:
    def __init__(self, start, end, board):
        self.start_row, self.start_col = start
        self.end_row, self.end_col = end
        self.origin, self.destination = board[self.start_row][self.start_col], board[self.end_row][self.end_col]
        self.board = board

    # Pawns can move forward one square if that square is unoccupied. They capture enemy pieces by moving diagonally
    # forward. Additionally, pawns on their starting square may move forward two spaces, providing both are unoccupied.
    # We need to check the colour of the pawn because pawns are the only piece that can't move backwards, so the
    # coordinate delta conditions will be different for white and black.

    def check_move(self):
        if self.origin == 'WP':
            if self.start_row == 6:  # Starting row for white in our code
                if self.end_row == 4 and self.start_col == self.end_col and self.destination == '~~' and \
                        self.board[self.end_row + 1][self.end_col] == '~~':  # Both squares in front of pawn empty
                    return True
                elif self.end_row == 5 and self.start_col == self.end_col and self.destination == '~~':
                    return True
                elif self.end_row == 5 and self.start_col - self.end_col in [-1, 1] and self.destination in \
                        black_pieces:  # Allows diagonal capture
                    return True
            else:
                if self.start_row - self.end_row == 1 and self.start_col == self.end_col and self.destination == '~~':
                    return True
                elif self.start_row - self.end_row == 1 and self.start_col - self.end_col in [-1, 1] and \
                        self.destination in black_pieces:
                    return True
        elif self.origin == 'BP':  # Same rules in reverse for black pawns
            if self.start_row == 1:
                if self.end_row == 3 and self.start_col == self.end_col and self.destination == '~~' and \
                        self.board[self.end_row - 1][self.end_col] == '~~':
                    return True
                elif self.end_row == 2 and self.start_col == self.end_col and self.destination == '~~':
                    return True
                elif self.end_row == 2 and self.start_col - self.end_col in [-1, 1] and self.destination in \
                        white_pieces:
                    return True
            else:
                if self.start_row - self.end_row == -1 and self.start_col == self.end_col and self.destination == '~~':
                    return True
                elif self.start_row - self.end_row == -1 and self.start_col - self.end_col in [-1, 1] and \
                        self.destination in white_pieces:
                    return True
        return False


class Knight:
    def __init__(self, start, end, board):
        self.start_row, self.start_col = start
        self.end_row, self.end_col = end
        self.origin, self.destination = board[self.start_row][self.start_col], board[self.end_row][self.end_col]

    # Knights can move horizontally once and vertically twice, or vice versa, in any direction, giving a total
    # of eight possible moves. We only need to check that the absolute deltas follow one of these two patterns
    # because the knight 'jumps' to its destination, so its path there is irrelevant.

    def check_move(self):
        # Check target square isn't occupied by friendly piece
        if (self.origin == 'WN' and self.destination not in white_pieces) or (self.origin == 'BN' and self.destination
                                                                              not in black_pieces):
            delta_row, delta_col = self.end_row - self.start_row, self.end_col - self.start_col
            return abs(delta_row) == 2 and abs(delta_col) == 1 or abs(delta_row) == 1 and abs(delta_col) == 2
        return False


class Bishop:
    def __init__(self, start, end, board):
        self.start_row, self.start_col = start
        self.end_row, self.end_col = end
        self.origin, self.destination = board[self.start_row][self.start_col], board[self.end_row][self.end_col]
        self.board = board

    # Bishops can move diagonally any number of squares in any direction. We need to check a) that the path between the
    # origin and destination is a valid diagonal and b) that there is no piece blocking that path.

    def check_move(self):
        if (self.origin == 'WB' and self.destination not in white_pieces) or (self.origin == 'BB' and self.destination
                                                                              not in black_pieces):
            delta_row, delta_col = abs(self.start_row - self.end_row), abs(self.start_col - self.end_col)
            if delta_row == delta_col:  # Can only be a valid diagonal move if column and row deltas are equal
                row_step, col_step = 1 if self.end_row > self.start_row else -1, 1 if self.end_col > self.start_col \
                    else -1  # The differences here dictate the direction of piece travel
                r, c = self.start_row + row_step, self.start_col + col_step
                while r != self.end_row and c != self.end_col:
                    if self.board[r][c] != '~~' and self.board[r][c] != self.destination:
                        return False  # If square is not empty or the target square, there must be a piece in the way
                    r, c = r + row_step, c + col_step
                return True
        return False


class Rook:
    def __init__(self, start, end, board):
        self.start_row, self.start_col = start
        self.end_row, self.end_col = end
        self.origin, self.destination = board[self.start_row][self.start_col], board[self.end_row][self.end_col]
        self.board = board

    # Rooks can move horizontally or vertically any number of squares. We need to check a) that the path passed is
    # either horizontal or vertical and b) that there is nothing in the way,

    def check_move(self):
        if (self.origin == 'WR' and self.destination not in white_pieces) or (self.origin == 'BR' and self.destination
                                                                              not in black_pieces):
            if self.start_col == self.end_col:  # Must be vertical line
                row_step = 1 if self.end_row > self.start_row else -1
                r = self.start_row + row_step
                while r != self.end_row:
                    if self.board[r][self.start_col] != '~~' and self.board[r][self.start_col] != self.destination:
                        return False
                    r += row_step
                return True
            elif self.start_row == self.end_row:  # Must be vertical line
                col_step = 1 if self.end_col > self.start_col else -1
                c = self.start_col + col_step
                while c != self.end_col:
                    if self.board[self.start_row][c] != '~~' and self.board[self.start_row][c]:
                        return False
                    c += col_step
                return True
        return False


class Queen:
    def __init__(self, start, end, board):
        self.start_row, self.start_col = start
        self.end_row, self.end_col = end
        self.origin, self.destination = board[self.start_row][self.start_col], board[self.end_row][self.end_col]
        self.board = board

    # Queens can move in any direction, any number of squares. Their move logic is therefore just a combination of a
    # rook and a bishop's.
    def check_move(self):
        if (self.origin == 'WQ' and self.destination not in white_pieces) or (self.origin == 'BQ' and self.destination
                                                                              not in black_pieces):
            if self.start_row == self.end_row or self.start_col == self.end_col:  # Check if valid rook move
                if self.start_col == self.end_col:  # Checks vertical path
                    row_step = 1 if self.end_row > self.start_row else -1
                    r = self.start_row + row_step
                    while r != self.end_row:
                        if self.board[r][self.start_col] != '~~' and self.board[r][self.start_col] != self.destination:
                            return False
                        r += row_step
                    return True
                elif self.start_row == self.end_row:  # Checks horizontal path
                    col_step = 1 if self.end_col > self.start_col else -1
                    c = self.start_col + col_step
                    while c != self.end_col:
                        if self.board[self.start_row][c] != '~~' and self.board[self.start_row][c]:
                            return False
                        c += col_step
                    return True
            else:  # Check if valid bishop move
                delta_row, delta_col = abs(self.start_row - self.end_row), abs(self.start_col - self.end_col)
                if delta_row == delta_col:  # Can only be a valid diagonal move if column and row deltas are equal
                    row_step, col_step = 1 if self.end_row > self.start_row else -1, 1 if self.end_col > \
                                                                                          self.start_col else -1
                    r, c = self.start_row + row_step, self.start_col + col_step
                    while r != self.end_row and c != self.end_col:
                        if self.board[r][c] != '~~' and self.board[r][c] != self.destination:
                            return False
                        r, c = r + row_step, c + col_step
                    return True
            return False


class King:
    def __init__(self, start, end, board):
        self.start_row, self.start_col = start
        self.end_row, self.end_col = end
        self.origin, self.destination = board[self.start_row][self.start_col], board[self.end_row][self.end_col]
        self.board = board

    # The king can move in any direction by one square. We just need to make sure the move requested has a maximum
    # delta of 1 and check whether the target is occupied by a friendly piece. We will handle 'check' restrictions in a
    # separate function
    def check_move(self):
        if (self.origin == 'WK' and self.destination not in white_pieces) or (self.origin == 'BK' and self.destination
                                                                              not in black_pieces):
            valid_moves = ((-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1))  # The 8 possible moves
            return (self.end_row - self.start_row, self.end_col - self.start_col) in valid_moves
        return False
