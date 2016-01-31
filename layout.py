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
    grid[5:5+5, 8:8+8] = block
    grid[5:5+5, 8*3:(8*3)+8] = block
    grid[5:5+5, 8*5:(8*5)+8] = block

    # row2
    grid[5*3:(5*3)+5, 8:8+8] = block
    grid[5*3:(5*3)+5, 8*3:(8*3)+8] = block
    grid[5*3:(5*3)+5, 8*5:(8*5)+8] = block

    # row3
    grid[5*5:(5*5)+5, 8:8+8] = block
    grid[5*5:(5*5)+5, 8*3:(8*3)+8] = block
    grid[5*5:(5*5)+5, 8*5:(8*5)+8] = block

    # TODO Given the time, let's make the grid rendering more sensible.
    # grid = threeby3(grid)

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
    main()