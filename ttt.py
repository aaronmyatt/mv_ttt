# # MV_TTT
#
# A simple tictactoe application demonstrating an (TODO:P) 'unbeatable' AI
# using the MinMac Algorith.
#
# Created for a chance at a Mindvalley career!
# By: Aaron Myatt.
#

# The beautiful handywork of Thomas Ballinger making this possible:
# https://github.com/thomasballinger/curtsies

from curtsies.fmtfuncs import *
from curtsies import FullscreenWindow, Input, fsarray

# and a little standard library!
import sys
from collections import OrderedDict
from itertools import permutations
import copy

coordinates = OrderedDict()
TURN = 'O'
ROUND = 0
BOARD = {}
oh_turn = fsarray(["""It's OH's turn"""])
ex_turn = fsarray(["""It's EX's turn"""])


def base():
    """
    Renders a large base/background grid
    """
    return fsarray([x * (7 * 8) for x in 'X' * (5 * 7)])


def block(char, height, width):
    """
    Clears space for O/X in the board background
    """
    return fsarray([x * width for x in char * height])


def make_grid(block):
    """
    insert blocks at specified intervals
    """
    grid = base()
    grid = render_rows(grid, block)

    return grid


def render_rows(grid, block, size=3):
    """
    Iteratively place blocks of `whitespace` to create a 3x3 grid
    """
    width = block.width
    height = block.height

    # for rows in grid size
    for row in [1, 3, 5]:
        # while there are columns to full.
        for column in [1, 3, 5]:
            from_top = height * row
            tuntil = (height * row) + height
            from_right = width * column
            wuntil = (width * column) + width

            # place block, block.height*row from top and block.width*column from right
            grid[from_top:tuntil, from_right:wuntil] = block

            # store block coordinates for later
            label = '{r}{c}'.format(r=row, c=column)
            coordinates[label] = (from_top, from_right)
    return grid


def all_ohs():
    """
    Test function to render all ohs on the grid
    """
    with FullscreenWindow() as window:
        b = make_grid(block(' ', 5, 8))
        while True:
            window.render_to_terminal(b)
            for k in coordinates:
                b = draw_oh(b, coordinates[k])
                window.render_to_terminal(b)


def all_exs():
    """
    Test function to render all exs on the grid
    """
    with FullscreenWindow() as window:
        b = make_grid(block(' ', 5, 8))
        while True:
            window.render_to_terminal(b)
            for k in coordinates:
                b = draw_exs(b, coordinates[k])
                window.render_to_terminal(b)


def draw_oh(grid, coord):
    """
    Build an `O` `FSArray` and attach to the base grid
    """
    oh = block('O', 5, 6)
    oh_inner = block(' ', 3, 4)
    oh[1:4, 1:5] = oh_inner

    height = coord[0]
    width = coord[1] + 1

    # place block, block.height*row from top and block.width*column from right
    grid[height:height + oh.height, width:width + oh.width] = oh
    return grid


def draw_exs(grid, coord):
    """
    Build an `X` `FSArray` and attach to the base grid
    """
    ex = block('`', 5, 6)
    ex[0:1, :] = fsarray(['\    /'])
    ex[1:2, :] = fsarray([' \  / '])
    ex[2:3, :] = fsarray(['  \/  '])
    ex[3:4, :] = fsarray(['  /\  '])
    # Strangely this last backspace was treated as an escape character by
    # the interpreter
    ex[4:5, :] = fsarray([' /  \\ '])

    height = coord[0]
    width = coord[1] + 1

    # place block, block.height*row from top and block.width*column from right
    grid[height:height + ex.height, width:width + ex.width] = ex
    return grid


def win_condition(board):
    '''
    Check all straight line combinations to determine if a player has won.

    >>> board = {1:'O', 2: 'O', 3:'O'}
    >>> win_condition(board)
    (True, (1, 2, 3))

    >>> board = {1:'O', 2: 'O', 3:'X'}
    >>> win_condition(board)
    False

    >>> board = {1:'O', 2: 'O', 3:'X', 7:'X', 8:'X', 9:'X'}
    >>> win_condition(board)
    (True, (7, 8, 9))
    '''

    # These are the only permutation that matter
    win_cond = ((1, 2, 3), (4, 5, 6), (7, 8, 9), (1, 4, 7), (2, 5, 8), (3, 6, 9), (1, 5, 9), (3, 5, 7))

    for each in win_cond:
        all_three = []
        try:
            for choice in each:
                # If the choice is not on the board, move on
                # and both players do not hold a position
                if choice in board and not ('X' in all_three and 'O' in all_three):
                    all_three.append(board[choice])
                else:
                    raise
            if 'X' in all_three and 'O' in all_three:
                # If we find both players, move on.
                raise
            # Otherwise someone has won
            return True, each
        except:
            pass
    return False


def log_board_layout(choice=None, player=None):
    '''
    Manages the players ex/oh placement persistence
    '''
    global BOARD
    if choice and player:
        BOARD[choice] = player
        return
    return BOARD

def alpha_go(grid, board):
    '''
    AI player. Should calculate the next best move through min-max ranking
    '''
    global TURN

    # calculate the best next move
    best_seq = minmax(copy.copy(log_board_layout()))
    next_move = list(best_seq).pop()

    # register the move as per a human player
    log_board_layout(next_move, 'X')
    choice = list(board.keys())[next_move]

    # Draw it to the grid
    grid = draw_exs(grid, board[choice])
    TURN = 'O'
    return grid

def value(board, player='X', round=None, layout=None):
    """
    Recursively determine the minmax value associated with a board
    permutation.
    """
    global ROUND
    if round == ROUND:
        layout = copy.copy(log_board_layout())
    layout[board.pop()] = player
    w = win_condition(layout)
    if w == player:
        return 1
    if w == "O":
        return -1
    if round > 8 or not board:
        return 0


    if player == 'X':
        return max([value(board, player, round+1, layout) for b in board])
    else:
        return min([value(board, "O", round+1, layout) for b in board])


def minmax(board, player='X'):
    """
    Returns best next board
    """
    global ROUND

    # Calculate all possible game permutations
    possible_moves = set(range(1,10)).difference(set(board.keys()))
    possible_games = permutations(possible_moves)
    return sorted(possible_games, key=lambda b: value(list(b), player, ROUND))[-1]


def main():
    global TURN, ROUND

    # 1) Start user/keyboard input handler
    with Input() as input:

        # 2) Start window/graphics manager
        with FullscreenWindow() as window:

            # 3) Build the initial view
            b = make_grid(block(' ', 5, 8))
            half_half = ' ' * int((b.width / 2) / 2)
            b[0:1, :] = fsarray(['{}PRESS A KEY TO GET STARTED'
                                .format(half_half)])
            b[b.height - 1:b.height, :] = fsarray(['{} It is round {}.'
                                                  .format(half_half, ROUND)])
            # 4) Draw initial screen
            window.render_to_terminal(b)

            # 5) Enter the main/game loop
            while True:

                # In the current implementation, playing beyond round 9 is
                # fruitless. However, we need a buffer to enable presentation
                # of the winner.
                if ROUND > 10:
                    sys.exit()

                # Check if a player has a winning row
                if win_condition(log_board_layout()):

                    # Due to the current ordering we need to switch around the players
                    if TURN=='O':
                        TURN="X"
                    else:
                        TURN="O"

                    # Clear the screen and announce winner
                    b = base()
                    b[0:1, :] = fsarray(['{}Player {} has won!.'
                                                  .format(half_half, TURN)])
                    window.render_to_terminal(b)
                    import time
                    time.sleep(3)
                    sys.exit()

                # 6) Game loop pauses on every pass to await the users next input
                if TURN == 'O':
                    c = input.next()

                    # Exits on Escape key press
                    if c == '' or c == '<ESC>':
                        sys.exit()

                    # Catch numeric input for determination of where
                    # to draw the ex's and oh's
                    # TODO prevent key presses overriding previous choices.
                    elif c in map('{}'.format, range(1, 10)) and ROUND > 0:
                        b[2:3, :] = fsarray(['{}You pressed key {}.'
                                            .format(half_half, c)])

                        coords = list(coordinates.keys())[int(c) - 1]
                        coords = coordinates[coords]

                        # Capture the players choice to help calculation of winning
                        # plays.
                        log_board_layout(int(c), TURN)
                        if TURN == 'O':
                            draw_oh(b, coords)
                            TURN = 'X'
                        else:
                            # draw_exs(b, coords)
                            TURN = 'O'
                        window.render_to_terminal(b)

                    # TODO Don't increment the round if a different key is pressed
                    # else:
                    #     continue

                b[b.height - 1:b.height, :] = fsarray(['{} It is round {}.'
                                                      .format(half_half, ROUND)])

                # Simple turn management using Global variables
                # TODO move this to a class to better handle state
                if TURN == 'O':
                    b[0:1, :] = oh_turn
                    b[1:2, :] = fsarray(['{}Press 1-9 to mark your location.'
                                        .format(half_half)])
                    window.render_to_terminal(b)
                    ROUND += 1
                    continue
                b[0:1, :] = ex_turn
                # A small homage to: http://deepmind.com/alpha-go.html
                b = alpha_go(b, coordinates)
                ROUND += 1
                window.render_to_terminal(b)



if __name__ == '__main__':
    main()
