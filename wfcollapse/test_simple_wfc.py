import os
import time

from board import Board2d
from superposition_tile import SuperpositionTile
from simple_wfc import SimpleCollapse


if __name__ != '__main__':
    raise RuntimeError('This file is not meant to be imported')


def draw_board(board: list[list[set[int]]]):
    for line in board:
        l1 = ""
        l2 = ""
        for el in line:
            lst = list(el)
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
    pass


test_simple_wfc()
