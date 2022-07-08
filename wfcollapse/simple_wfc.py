from __future__ import annotations

from random import choice

from .board import Board2d, BoardTile
from .superposition_tile import SuperpositionTile
from .wfc_abstract import WFCAbstract


class SimpleCollapse(WFCAbstract):
    def __init__(self, board: Board2d[SuperpositionTile], rules: dict[int, set[int]]):
        super().__init__(board)
        self.rules: dict[int, set[int]] = {}

        for v in rules:
            if v not in self.rules:
                self.rules[v] = set()

            for v2 in rules[v]:
                if v2 not in self.rules:
                    self.rules[v2] = set()

                self.rules[v].add(v2)
                self.rules[v2].add(v)

    def solve_tile(self, tile: BoardTile[SuperpositionTile]):
        neighbours = tile.neighbours()
        to_discard = set()

        for neighbour in neighbours:
            for superposition in tile.tile.superpositions:
                if (not neighbour.tile.unsolvable) and \
                        not self.rules[superposition].intersection(neighbour.tile.superpositions):
                    to_discard.add(superposition)

        tile.tile.superpositions.difference_update(to_discard)
        return bool(to_discard)

    def collapse_tile(self, tile: BoardTile[SuperpositionTile]):
        if not tile.tile.collapsed:
            tile.tile.superpositions = {choice(list(tile.tile.superpositions))}

    def select_tile_to_collapse(self, tiles: set[BoardTile[SuperpositionTile]]) -> BoardTile[SuperpositionTile]:
        return tiles.pop()


__all__ = ['SimpleCollapse']
