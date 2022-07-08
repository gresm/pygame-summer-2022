from __future__ import annotations

import os
import time

from wfcollapse.board import Board2d, BoardTile
from wfcollapse.superposition_tile import SuperpositionTile
from wfcollapse.simple_wfc import SimpleCollapse
from wfcollapse.wfc import Collapse, CollapseRules
from argparse import ArgumentParser

if __name__ != '__main__':
    raise RuntimeError('This file is not meant to be imported')


def in_color(text: str, foreground, background):
    mat = f'\33[38;2;{";".join(map(str, foreground))};48;2;{";".join(map(str, background))}m'
    return f"{mat}{text}\33[0m"


def draw_board(board: list[list[BoardTile[SuperpositionTile]]], states: int, tile_width: int,
               mark: tuple[int, int] | None = None):
    colors_list = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 0), (0, 255, 0), (0, 0, 255), (0, 0, 255),
                   (0, 0, 255),
                   (255, 255, 0), (255, 0, 255),
                   (0, 255, 255), (128, 128, 128),
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


parser = ArgumentParser()
parser.add_argument('-w', '--width', type=int, default=10)
parser.add_argument('-hg', '--height', type=int, default=10)
parser.add_argument('-i', '--immediate', action='store_true')
parser.add_argument('-d', '--delay', type=float, default=0.1)
parser.add_argument('--complex-test', action='store_true')
args = parser.parse_args()

sleep = args.delay
immediate = args.immediate
width = args.width
height = args.height
run_complex_test = args.complex_test


def frame():
    time.sleep(sleep)
    os.system('clear' if os.name == 'posix' else 'cls')


def test_simple_wfc():
    collapse = SimpleCollapse(Board2d(width, height, SuperpositionTile({0, 1, 2, 3})),
                              {0: {0}, 1: {1, 0}, 2: {1, 2}, 3: {2, 3}})

    inc = 0

    for step in collapse.solve():
        board = [[False for _ in range(collapse.board.width)] for _ in range(collapse.board.height)]
        for pos in step:
            if not immediate:
                board[pos[0]][pos[1]] = True
                frame()
                draw_board(collapse.board.board, 9, 3, pos)
                print("step: ", inc)
                print("visited: ")
                draw_visits_board(board)
        inc += 1

    if not immediate:
        frame()
    draw_board(collapse.board.board, 9, 3)


def test_complex_wfc():
    collapse = Collapse(Board2d(width, height, SuperpositionTile({0, 1, 2, 3, 4, 5, 6, 7})), CollapseRules.parse(
        {0: (0, 0, 0, 0), 1: (1, 1, 1, 0), 2: (2, 2, 2, 1), 3: (1, 1, 0, 0), 4: (0, 1, 0, 0), 5: (2, 2, 1, 1),
         6: (1, 2, 2, 1), 7: (2, 2, 2, 2)}))

    inc = 0

    for step in collapse.solve():
        board = [[False for _ in range(collapse.board.width)] for _ in range(collapse.board.height)]
        for pos in step:
            if not immediate:
                board[pos[0]][pos[1]] = True
                frame()
                draw_board(collapse.board.board, 4, 2, pos)
                print("step: ", inc)
                print("visited: ")
                draw_visits_board(board)
        inc += 1

    if not immediate:
        frame()
    draw_board(collapse.board.board, 4, 2)


try:
    if run_complex_test:
        test_complex_wfc()
    else:
        test_simple_wfc()
except KeyboardInterrupt:
    print("Interrupted, exiting...")
    exit(1)
