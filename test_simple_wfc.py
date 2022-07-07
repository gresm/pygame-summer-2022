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


def draw_board(board: list[list[BoardTile[SuperpositionTile]]], states: int, mark: tuple[int, int] | None = None):
    tile_width = (states + 1) // 2
    colors_list = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255), (128, 128, 128),
                   (128, 0, 0), (0, 128, 0), (0, 0, 128), (128, 128, 0), (128, 0, 128), (0, 128, 128), (128, 128, 128)]

    for x in range(len(board)):
        str_rows: list[str] = ["" for _ in range(tile_width)]
        for y in range(len(board[x])):
            tile = board[x][y]
            sups = list(tile.tile.superpositions)
            sups.sort()
            ind = 0
            for sup_ind in range(states):
                colored_text = f'{str(sups[sup_ind]) if len(sups) > sup_ind else "."} '
                if (x, y) == mark:
                    colored_text = in_color(colored_text, (0, 0, 0), (255, 255, 255))
                elif tile.tile.entropy() == 1:
                    colored_text = in_color(colored_text, (0, 0, 0), colors_list[tile.tile.superpositions.copy().pop()])
                str_rows[ind] += colored_text
                ind += 1
                if ind >= tile_width:
                    ind = 0

            for ind in range(len(str_rows)):
                str_rows[ind] += "  "

        for row in str_rows:
            print(row)
        print()


def draw_visits_board(board: list[list[bool]]):
    for line in board:
        for el in line:
            print('x' if el else '.', end='')
        print()


sleep = 0.05
immediate = input("Immediate? (y/n) ").lower().startswith("y")


def frame():
    time.sleep(sleep)
    os.system('clear' if os.name == 'posix' else 'cls')


def test_simple_wfc():
    collapse = SimpleCollapse(Board2d(10, 10, SuperpositionTile({0, 1, 2, 3})),
                              {0: {0}, 1: {1, 0}, 2: {1, 2}, 3: {2, 3}})

    frame()
    draw_board(collapse.board.board, 4)
    inc = 0

    for step in collapse.solve():
        board = [[False for _ in range(10)] for _ in range(10)]
        for pos in step:
            if not immediate:
                board[pos[0]][pos[1]] = True
                frame()
                draw_board(collapse.board.board, 4, pos)
                print("step: ", inc)
                print("visited: ")
                draw_visits_board(board)
        inc += 1

    frame()
    draw_board(collapse.board.board, 4)


test_simple_wfc()