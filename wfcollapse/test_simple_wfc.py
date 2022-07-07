import os
import time

from board import Board2d, BoardTile
from superposition_tile import SuperpositionTile
from simple_wfc import SimpleCollapse


if __name__ != '__main__':
    raise RuntimeError('This file is not meant to be imported')


def draw_board(board: list[list[BoardTile[SuperpositionTile]]]):
    for line in board:
        l1 = ""
        l2 = ""
        for el in line:
            lst = list(el.tile.superpositions)
            lst.sort()
            l1 += str(lst[0]) if len(lst) > 0 else "."
            l1 += str(lst[1]) if len(lst) > 1 else "."
            l2 += str(lst[2]) if len(lst) > 2 else "."
            l2 += str(lst[3]) if len(lst) > 3 else "."
        print(l1)
        print(l2)


sleep = 0.05


def frame():
    os.system('clear' if os.name == 'posix' else 'cls')
    time.sleep(sleep)


def test_simple_wfc():
    collapse = SimpleCollapse(Board2d(10, 10, SuperpositionTile({0, 1, 2, 3})),
                              {0: {2, 3}, 1: {1, 2, 3}, 2: set(), 3: set()})

    draw_board(collapse.board.board)

    for board in collapse.solve():
        frame()
        draw_board(board)

    draw_board(collapse.board.board)


test_simple_wfc()
