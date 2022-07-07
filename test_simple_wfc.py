from __future__ import annotations

import os
import time

from wfcollapse.board import Board2d, BoardTile
from wfcollapse.superposition_tile import SuperpositionTile
from wfcollapse.simple_wfc import SimpleCollapse

if __name__ != '__main__':
    raise RuntimeError('This file is not meant to be imported')


def in_color(text: str, foreground, background):
    mat = f'\33[38;2;{";".join(map(str, foreground))};48;2;{";".join(map(str, background))}m'
    return f"{mat}{text}\33[0m"


def draw_board(board: list[list[BoardTile[SuperpositionTile]]], mark: tuple[int, int] | None = None):
    for x in range(len(board)):
        line = board[x]
        l1 = ""
        l2 = ""
        for y in range(len(line)):
            el = line[y]
            lst = list(el.tile.superpositions)
            lst.sort()

            el_l1 = str(lst[0]) if len(lst) > 0 else '.'
            el_l1 += str(lst[1]) if len(lst) > 1 else "."
            el_l2 = str(lst[2]) if len(lst) > 2 else "."
            el_l2 += str(lst[3]) if len(lst) > 3 else "."

            if mark is not None and x == mark[0] and y == mark[1]:
                el_l1 = in_color(el_l1, (0, 0, 0), (255, 255, 255))
                el_l2 = in_color(el_l2, (0, 0, 0), (255, 255, 255))

            l1 += el_l1
            l2 += el_l2

            l1 += " "
            l2 += " "
        print(l1)
        print(l2)
        print()


def draw_visits_board(board: list[list[bool]]):
    for line in board:
        for el in line:
            print('x' if el else '.', end='')
        print()


sleep = 0.05


def frame():
    time.sleep(sleep)
    os.system('clear' if os.name == 'posix' else 'cls')


def test_simple_wfc():
    collapse = SimpleCollapse(Board2d(10, 10, SuperpositionTile({0, 1, 2, 3})),
                              {0: {0}, 1: {1, 0}, 2: {1, 2}, 3: {2, 3}})

    frame()
    draw_board(collapse.board.board)
    inc = 0

    for step in collapse.solve():
        board = [[False for _ in range(10)] for _ in range(10)]
        for pos in step:
            board[pos[0]][pos[1]] = True
            frame()
            draw_board(collapse.board.board, pos)
            print("step: ", inc)
            print("visited: ")
            draw_visits_board(board)
        inc += 1

    frame()
    draw_board(collapse.board.board)


test_simple_wfc()
