from random import choice

from .board import Board2d, BoardTile
from .superposition_tile import SuperpositionTile
from .wfcollapse import WFCAbstract


class SimpleCollapse(WFCAbstract):
    def __init__(self, board: Board2d[SuperpositionTile], rules: dict[int, set[int]]):
        super().__init__(board)
        self.rules = {v: set() for v in set(rules.keys()).union(rules.values())}

        for v in rules:
            for v2 in rules[v]:
                self.rules[v].add(v2)
                self.rules[v2].add(v)

    def solve_tile(self, tile: BoardTile[SuperpositionTile]):
        neighbours = tile.neighbours()
        to_discard = set()

        for neighbour in neighbours:
            for superposition in tile.tile.superpositions:
                if self.rules[superposition].intersection(neighbour.tile.superpositions):
                    to_discard.add(superposition)

        tile.tile.superpositions.difference_update(to_discard)

    def collapse_tile(self, tile: BoardTile[SuperpositionTile]):
        tile.tile.superpositions = {choice(list(tile.tile.superpositions))}

    def select_tile_to_collapse(self, tiles: set[BoardTile[SuperpositionTile]]) -> BoardTile[SuperpositionTile]:
        return tiles.pop()
