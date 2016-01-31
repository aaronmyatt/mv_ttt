import sys

from curtsies.fmtfuncs import *
from curtsies import FullscreenWindow, Input, fsarray
from collections import OrderedDict

coordinates = OrderedDict()

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
    with Input() as input:
        with FullscreenWindow() as window:
            b = make_grid(block(' ', 5, 8))
            while True:
                window.render_to_terminal(b)
                # if b.turn == 9 or b.winner():
                #     c = input.next() # hit any key
                #     sys.exit()
                while True:
                    c = input.next()
                    if c == '':
                        sys.exit()
                #     try:
                #         if int(c) in range(9):
                #             b = b.move(int(c))
                #     except ValueError:
                #         window.render_to_terminal(fsarray([blue("ELLOR!")]))
                #         time.sleep(1)
                #         window.render_to_terminal(b.display())
                #         continue
                #     window.render_to_terminal(b.display())
                #     break
                # if b.turn == 9 or b.winner():
                #     c = input.next() # hit any key
                #     sys.exit()
                # b = ai(b, 'o')

if __name__ == '__main__':
    all_exs()