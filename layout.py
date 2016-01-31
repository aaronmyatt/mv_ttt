import sys

from curtsies.fmtfuncs import *
from curtsies import FullscreenWindow, Input, fsarray


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
    width = int(block.width)
    height = int(block.height)
    grid = base()

    # row1 (5down, 10down, 8over, 16over)
    # grid[5:5+5, 8:8+8] = block
    # grid[5:5+5, 8*3:(8*3)+8] = block
    # grid[5:5+5, 8*5:(8*5)+8] = block
    #
    # # row2
    # grid[5*3:(5*3)+5, 8:8+8] = block
    # grid[5*3:(5*3)+5, 8*3:(8*3)+8] = block
    # grid[5*3:(5*3)+5, 8*5:(8*5)+8] = block
    #
    # # row3
    # grid[5*5:(5*5)+5, 8:8+8] = block
    # grid[5*5:(5*5)+5, 8*3:(8*3)+8] = block
    # grid[5*5:(5*5)+5, 8*5:(8*5)+8] = block

    # TODO Given the time, let's make the grid rendering more sensible.
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
    return grid


def all_ohs():
    with Input() as input:
        with FullscreenWindow() as window:
            b = make_grid(block(' ', 5, 8))
            while True:
                window.render_to_terminal(b)
                for coord in threeby3():
                    draw_oh(coord)

def place_oh(grid, coord):
    oh = block('O', 4, 7)
    oh_inner = block(' ', 2, 3)
    oh[1:3, 2:5] = oh_inner

    grid[coord[0]:coord[0]+5, 8:8+8] = oh

def place_ex(grid, coord):
    pass


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
    main()