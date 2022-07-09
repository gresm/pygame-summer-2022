from __future__ import annotations

import os
import time

from wfcollapse.board import Board2d, BoardTile
from wfcollapse.superposition_tile import SuperpositionTile
from wfcollapse import simple_wfc, wfc_old, wfc
from argparse import ArgumentParser

if __name__ != '__main__':
    raise RuntimeError('This file is not meant to be imported')


def in_color(text: str, foreground, background):
    mat = f'\33[38;2;{";".join(map(str, foreground))};48;2;{";".join(map(str, background))}m'
    return f"{mat}{text}\33[0m"


colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 0), (255, 255, 0), (255, 0, 255), (0, 255, 255),
          (128, 128, 128), (128, 0, 0), (0, 128, 0), (0, 0, 128), (128, 128, 0), (128, 0, 128),
          (0, 128, 128), (128, 128, 128)]
simple_colors = [colors[2], colors[4], colors[1], colors[0]]
wfc_colors = [colors[0], *[colors[1]] * 7]


def draw_board(colors_list: list[tuple[int, int, int]], board: list[list[BoardTile[SuperpositionTile]]], states: int,
               tile_width: int, mark: tuple[int, int] | None = None):
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
parser.add_argument('-w', '--width', type=int, default=10, help='width of the board')
parser.add_argument('-hg', '--height', type=int, default=10, help='height of the board')
parser.add_argument('-i', '--immediate', action='store_true', default=False, help='draw board immediately')
parser.add_argument('-d', '--delay', type=float, default=0.1, help='delay between steps')
parser.add_argument(
    '-a', '--algo', '--algorithm', type=int, choices=[0, 1, 2], default=0, help='0: simple, 1: old, 2: new'
)
args = parser.parse_args()

sleep = args.delay
immediate = args.immediate
width = args.width
height = args.height


def frame():
    time.sleep(sleep)
    os.system('clear' if os.name == 'posix' else 'cls')


def test_simple_wfc():
    collapse = simple_wfc.SimpleCollapse(Board2d(width, height, SuperpositionTile({0, 1, 2, 3})),
                                         {0: {0, 1}, 1: {1, 0}, 2: {1, 2, 3}, 3: {3}})

    inc = 0

    for step in collapse.solve():
        board = [[False for _ in range(collapse.board.width)] for _ in range(collapse.board.height)]
        for pos in step:
            if not immediate:
                board[pos[0]][pos[1]] = True
                frame()
                draw_board(simple_colors, collapse.board.board, 9, 3, pos)
                print("step: ", inc)
                print("visited: ")
                draw_visits_board(board)
        inc += 1

    if not immediate:
        frame()
    draw_board(simple_colors, collapse.board.board, 9, 3)


def test_old_wfc():
    collapse = wfc_old.Collapse(Board2d(width, height, SuperpositionTile({0, 1, 2, 3, 4, 5, 6, 7})),
                                wfc_old.CollapseRules.parse(
                                    {0: (0, 0, 0, 0), 1: (1, 1, 1, 0), 2: (2, 2, 2, 1), 3: (1, 1, 0, 0),
                                     4: (0, 1, 0, 0), 5: (2, 2, 1, 1), 6: (1, 2, 2, 1), 7: (2, 2, 2, 2)}))

    inc = 0

    for step in collapse.solve():
        board = [[False for _ in range(collapse.board.width)] for _ in range(collapse.board.height)]
        for pos in step:
            if not immediate:
                board[pos[0]][pos[1]] = True
                frame()
                draw_board(colors, collapse.board.board, 4, 2, pos)
                print("step: ", inc)
                print("visited: ")
                draw_visits_board(board)
        inc += 1

    if not immediate:
        frame()
    draw_board(colors, collapse.board.board, 4, 2)


def test_wfc():
    rules = wfc.CollapseRules()

    around = wfc.SideGroup(rules)
    inside = wfc.SideGroup(rules)

    around_tile = wfc.TileRule(rules, around, around, around, around, 10)
    inside_top = wfc.TileRule(rules, around, around, around, inside)
    inside_bottom = wfc.TileRule(rules, around, inside, around, around)
    inside_left = wfc.TileRule(rules, around, around, inside, around)
    inside_right = wfc.TileRule(rules, inside, around, around, around)
    inside_middle = wfc.TileRule(rules, inside, inside, inside, inside)

    rules.add(around_tile, inside_top, inside_bottom, inside_left, inside_right, inside_middle)

    collapse = wfc.Collapse(Board2d(width, height, SuperpositionTile(rules.get_superpositions())), rules)

    inc = 0

    for step in collapse.solve():
        board = [[False for _ in range(collapse.board.width)] for _ in range(collapse.board.height)]
        for pos in step:
            if not immediate:
                board[pos[0]][pos[1]] = True
                frame()
                draw_board(wfc_colors, collapse.board.board, 9, 3, pos)
                print("step: ", inc)
                print("visited: ")
                draw_visits_board(board)
        inc += 1

    if not immediate:
        frame()
    draw_board(wfc_colors, collapse.board.board, 9, 3)


try:
    tests = [test_simple_wfc, test_old_wfc, test_wfc]
    tests[args.algo]()
except KeyboardInterrupt:
    print("Interrupted, exiting...")
    exit(1)
