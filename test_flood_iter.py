import os
import time

from wfcollapse.flood_iter import Flood, FloodIter

if __name__ != '__main__':
    raise RuntimeError('This file is not meant to be imported')


def draw_board(board: list[list[bool]]):
    for line in board:
        for el in line:
            print('x' if el else '.', end='')
        print()


sleep = 0.05


def frame():
    time.sleep(sleep)
    os.system('clear' if os.name == 'posix' else 'cls')


# Test the flood_iter module
def test_iter():
    flood_settings = Flood(4, 4, -1)
    flood = FloodIter(flood_settings)
    board = [[False for _ in range(10)] for _ in range(10)]
    tiles = {(3, 3), (3, 4), (3, 5), (3, 6)}

    draw_board(board)
    frame()

    for pos, move in flood:
        move.all_true()
        move.eliminate_directions(*flood.tiles_limiter(pos, tiles))
        move.eliminate_directions(*flood.box_limiter(pos, 0, 0, 10, 10))
        board[pos[0]][pos[1]] = True

        draw_board(board)
        print(pos)
        frame()

    draw_board(board)


test_iter()
