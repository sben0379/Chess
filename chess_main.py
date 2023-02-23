"""This file acts as the main driver for our chess game. It handles the running of the game, user inputs and displaying
the game graphically to the user. It gets the piece restrictions from the chess_pieces module, and the state of the
 board and other important information (location of pieces rules like check, etc.) from the game_state module. """

from chess_game_state import GameState
from chess_pieces import King, Queen, Rook, Bishop, Knight, Pawn
import pygame

# We start by defining the board dimensions and initialising a dictionary that will store the piece images.

width = height = 512
sq_size = height // 8
images = {}
white_pieces = ['WP', 'WN', 'WB', 'WR', 'WQ', 'WK']
black_pieces = ['BP', 'BN', 'BB', 'BR', 'BQ', 'BK']


# The load_images() function loops through the list of pieces and assigns each the relevant image stored in the
# images files as their values.
def load_images():
    pieces = white_pieces + black_pieces
    for piece in pieces:
        images[piece] = pygame.transform.scale(pygame.image.load('/Users/james/Desktop/Python Projects/Chess/Images/' +
                                                                 piece + '.png'), (sq_size, sq_size))


# The render_board() function draws the board by alternating colours on odd and even squares, based on the screen size.
def render_board(screen):
    for row in range(8):
        for col in range(8):
            color = pygame.Color('white') if (row + col) % 2 == 0 else pygame.Color('dark green')
            pygame.draw.rect(screen, color, pygame.Rect(row * sq_size, col * sq_size, sq_size, sq_size))


# The render_pieces() function blits the corresponding image of the piece occupying each square onto the board, relative
# to the state of the board as tracked by the GameState module.
def render_pieces(screen, board):
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece != '~~':
                screen.blit(images[piece], pygame.Rect(col * sq_size, row * sq_size, sq_size, sq_size))


# The render_game_state() function combines the above functions and is called to update the graphical representation
# of the board to the user after each move.
def render_game_state(screen, gs):
    render_board(screen)
    render_pieces(screen, gs.board)
    pygame.display.update()


# The main() function handles the running of the game. We start by initialising GameState and display the board and
# pieces to the user. While the game is running, we accept user input in the form of a double click: first on the piece
# they wish to move and the second click on the target square. We then call the relevant methods from the game_state
# module to evaluate whether the request constitutes a legal move. If it does, we execute the move and graphically
# represent it to the user.
def main():
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    game = GameState()  # gs is now an instance of the game
    future_board = game.future_board()
    load_images()
    piece_classes = {  # Now when we check what piece code is at a square, we can evaluate its move restrictions too.
        'WP': Pawn,
        'BP': Pawn,
        'WN': Knight,
        'BN': Knight,
        'WB': Bishop,
        'BB': Bishop,
        'WR': Rook,
        'BR': Rook,
        'WQ': Queen,
        'BQ': Queen,
        'WK': King,
        'BK': King
    }
    move_queue = []  # Keeps track of last two clicks to determine the move intended
    turns = 0
    colours = ['W', 'B']  # List will be used to keep track of whose turn it is
    colour = colours[0]  # White always starts
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:  # Getting user mouse input
                x, y = pygame.mouse.get_pos()
                row = y // sq_size
                col = x // sq_size
                sq_clicked = (row, col)  # xy coordinates of the square clicked
                move_queue.append(sq_clicked)
                if len(move_queue) == 2:  # Call move function after second click
                    piece_code = game.board[move_queue[0][0]][move_queue[0][1]]
                    if piece_code in piece_classes:
                        piece_class = piece_classes[piece_code]
                        piece_selected = piece_class(move_queue[0], move_queue[1], game.board)
                        if piece_selected.check_move() and game.check_turn(colour, move_queue[0]):
                            future_board.make_move(move_queue[0], move_queue[1])
                            if not future_board.in_check(colour):
                                game.make_move(move_queue[0], move_queue[1])
                                turns += 1
                                if turns % 2 == 0:
                                    colour = colours[0]  # White's turn next
                                else:
                                    colour = colours[1]  # Black's turn next
                                move_queue = []  # Reset variable to be used for the next move
                            else:
                                print('King is in check!')
                                future_board = game.future_board()
                                move_queue = []
                        else:
                            move_queue = []
        render_game_state(screen, game)
    pygame.quit()


main()
