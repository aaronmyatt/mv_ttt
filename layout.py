import sys

from curtsies.fmtfuncs import *
from curtsies import FullscreenWindow, Input, fsarray
from collections import OrderedDict

coordinates = OrderedDict()
TURN = 'O'
oh_turn = fsarray(['''It's OH's turn'''])
ex_turn = fsarray(['''It's EX's turn'''])

def base():
    return fsarray([x*(7*8) for x in 'X'*(5*7)])

def block(char, height, width):
    '''
    space for O/X in the board background
    '''
    return fsarray([x*width for x in char*height])

def make_grid(block):
    '''
    insert blocks at specified intervals
    '''

    grid = base()
    grid = render_rows(grid, block)

    return grid

def render_rows(grid, block, size=3):
    width = block.width
    height = block.height

    # for rows in grid size
    for row in [1,3,5]:
        # while there are columns to full
        for column in [1,3,5]:
            from_top = height*row
            tuntil = (height*row)+height
            from_right = width*column
            wuntil = (width*column)+width

            # place block, block.height*row from top and block.width*column from right
            grid[from_top:tuntil, from_right:wuntil] = block

            # store block coordinates for later
            label = '{r}{c}'.format(r=row,c=column)
            coordinates[label] = (from_top, from_right)
    return grid


def all_ohs():
    with FullscreenWindow() as window:
        b = make_grid(block(' ', 5, 8))
        while True:
            window.render_to_terminal(b)
            for k in coordinates:
                b = draw_oh(b, coordinates[k])
                window.render_to_terminal(b)


def all_exs():
    with FullscreenWindow() as window:
        b = make_grid(block(' ', 5, 8))
        while True:
            window.render_to_terminal(b)
            for k in coordinates:
                b = draw_exs(b, coordinates[k])
                window.render_to_terminal(b)

def draw_oh(grid, coord):
    oh = block('O', 5, 6)
    oh_inner = block(' ', 3, 4)
    oh[1:4, 1:5] = oh_inner

    height = coord[0]
    width = coord[1]+1

    # place block, block.height*row from top and block.width*column from right
    grid[height:height+oh.height, width:width+oh.width] = oh
    return grid

def draw_exs(grid, coord):
    ex = block('`', 5, 6)
    ex[0:1, :] = fsarray(['\    /'])
    ex[1:2, :] = fsarray([' \  / '])
    ex[2:3, :] = fsarray(['  \/  '])
    ex[3:4, :] = fsarray(['  /\  '])
    ex[4:5, :] = fsarray([' /  \\ '])
    
    height = coord[0]
    width = coord[1]+1

    # place block, block.height*row from top and block.width*column from right
    grid[height:height+ex.height, width:width+ex.width] = ex
    return grid


def main():
    global TURN
    with Input() as input:
        with FullscreenWindow() as window:
            b = make_grid(block(' ', 5, 8))
            half_half = ' '*int((b.width/2)/2)
            b[0:1, :] = fsarray(['{}PRESS A KEY TO GET STARTED'
                                .format(half_half)])
            window.render_to_terminal(b)
            while True:
                c = input.next()
                if c == '' or c == '<ESC>':
                    sys.exit()

                if TURN == 'O':
                    b[0:1, :] = oh_turn
                    window.render_to_terminal(b)
                    TURN = 'X'
                    continue
                b[0:1, :] = ex_turn
                window.render_to_terminal(b)
                TURN='O'
                continue


if __name__ == '__main__':
    main()