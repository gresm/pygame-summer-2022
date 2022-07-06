import os
import time

from flood_iter import Flood, FloodIter

if __name__ != '__main__':
    raise RuntimeError('This file is not meant to be imported')


def draw_board(board: list[list[int]]):
    for line in board:
        for el in line:
            print('x' if el else ' ', end='')
        print()


# Test the flood_iter module
def test_iter():
    print("start")
    flood_settings = Flood(4, 4, -1)
    flood = FloodIter(flood_settings)
    board = [[False for _ in range(10)] for _ in range(10)]

    for pos, move in flood:
        draw_board(board)
        time.sleep(0.1)
        os.system('clear')
        move.all_true()
        move.eliminate_directions(*flood.box_limiter(pos, 0, 0, 9, 9))
        print(pos)
        board[pos[0]][pos[1]] = True


test_iter()
