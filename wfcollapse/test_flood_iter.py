import os
import time

from flood_iter import Flood, FloodIter

if __name__ != '__main__':
    raise RuntimeError('This file is not meant to be imported')


def draw_board(board: list[list[int]]):
    for line in board:
        for el in line:
            print('x' if el else '.', end='')
        print()


# Test the flood_iter module
def test_iter():
    print("start")
    flood_settings = Flood(4, 4, -1)
    flood = FloodIter(flood_settings)
    board = [[False for _ in range(10)] for _ in range(10)]
    sleep = 0.05

    os.system('clear')
    draw_board(board)
    time.sleep(sleep)

    for pos, move in flood:
        move.all_true()
        move.eliminate_directions(*flood.box_limiter(pos, 0, 0, 10, 10))
        board[pos[0]][pos[1]] = True

        os.system('clear')
        draw_board(board)
        print(pos)
        time.sleep(sleep)


test_iter()
