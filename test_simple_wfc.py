from __future__ import annotations

import os
import time

from wfcollapse.board import Board2d, BoardTile
from wfcollapse.superposition_tile import SuperpositionTile
from wfcollapse.simple_wfc import SimpleCollapse


if __name__ != '__main__':
    raise RuntimeError('This file is not meant to be imported')


def draw_board(board: list[list[BoardTile[SuperpositionTile]]]):
    for line in board:
        l1 = ""
        l2 = ""
        for el in line:
            lst = list(el.tile.superpositions)
            lst.sort()

            l1 += str(lst[0]) if len(lst) > 0 else '.'
            l1 += str(lst[1]) if len(lst) > 1 else "."
            l2 += str(lst[2]) if len(lst) > 2 else "."
            l2 += str(lst[3]) if len(lst) > 3 else "."

            l1 += " "
            l2 += " "
        print(l1)
        print(l2)
        print()


sleep = 0.1


def frame():
    time.sleep(sleep)
    os.system('clear' if os.name == 'posix' else 'cls')


def test_simple_wfc():
    collapse = SimpleCollapse(Board2d(10, 10, SuperpositionTile({0, 1, 2, 3})),
                              {0: set(), 1: set(), 2: set(), 3: set()})

    frame()
    draw_board(collapse.board.board)
    inc = 0

    for step in collapse.solve():
        for _ in step:
            pass
        frame()
        draw_board(collapse.board.board)
        print("step: ", inc)
        inc += 1

    frame()
    draw_board(collapse.board.board)


test_simple_wfc()
