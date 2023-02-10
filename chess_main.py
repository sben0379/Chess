"""
This is the main file that will handle the user's interaction with the game: user inputs, displaying the game state,
and so on.
"""
import pygame

# To start drawing out the board, we will specify the size of the board and the squares. We will also create a
# dictionary to map each piece code to the corresponding image.

width = height = 512
sq_size = height // 8
images = {}


# Define load images function to loop through list of pieces and set the value to each piece key in the dictionary to
# the corresponding image.

def load_images():
    pieces = ['WK', 'WQ', 'WR', 'WB', 'WN', 'WP', 'BK', 'BQ', 'BR', 'BB', 'BN', 'BP']
    for piece in pieces:
        images[piece] = pygame.transform.scale(pygame.image.load('/Users/james/Desktop/Python Projects/Chess/Images/' +
                                                                 piece + '.png'), (sq_size, sq_size))


# Create a class GameState that will keep track of the board and position of the pieces at all times. The board is in
# the form of an 8x8 2D list where each piece is represented by a code and empty squares are represented by ##. The
# starting position can thus be represented as follows.

class GameState():
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


# Define main function to act as our driver for the game. We'll start by setting up the screen and importing the game
# state from our chess engine file.

def main():
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    gs = GameState()
    load_images()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        render_game_state(screen, gs)
    pygame.quit()


# Define render board function to alternate colours from squares to square. If we assign each row and each column a
# number 1-9, we can alternate colours with a nested loop by checking whether a square is even or odd.

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
