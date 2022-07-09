from __future__ import annotations

from random import choice
from .wfc_abstract import WFCAbstract
from .board import Board2d, BoardTile
from .superposition_tile import SuperpositionTile

_TileSideFormat = int

_TileRulesFormat = tuple[
    _TileSideFormat,  # left
    _TileSideFormat,  # top
    _TileSideFormat,  # right
    _TileSideFormat,  # bottom
]


class TileRules:
    def __init__(self, rules: tuple[int, int, int, int]):
        self.rules = rules

    def __str__(self):
        return str(self.rules)

    def __repr__(self):
        return str(self)

    def __getitem__(self, item):
        return self.rules[item]

    def compare(self, collapse_rules: CollapseRules, tile_type: int, side: int) -> bool:
        return collapse_rules.rules[tile_type][side] == self[(side - 2) % 4]


class CollapseRules:
    def __init__(self, rules: dict[int, TileRules], chance: dict[int, int] | None = None):
        self.rules = rules
        self.chance = chance

    @classmethod
    def parse(cls, rules: dict[int, _TileRulesFormat], chance: dict[int: int] | None = None):
        rules_dict = {r: TileRules(rules[r]) for r in rules}
        return cls(rules_dict, chance)

    def collapse(self, superpositions: set[int], orientation: int, tile_type: set[int]):
        if not len(tile_type):
            return superpositions

        valid: set[int] = set()

        for superposition in superpositions:
            for tile in tile_type:
                if self.rules[superposition].compare(self, tile, orientation):
                    valid.add(superposition)
        return valid

    def collapse_around(self, tile: BoardTile[SuperpositionTile]) -> set[int]:
        ret = tile.tile.superpositions

        if tile.tile.collapsed:
            return ret

        if tile.left:
            ret = self.collapse(ret, 0, tile.left.tile.superpositions)
        if tile.right:
            ret = self.collapse(ret, 2, tile.right.tile.superpositions)
        if tile.up:
            ret = self.collapse(ret, 1, tile.up.tile.superpositions)
        if tile.down:
            ret = self.collapse(ret, 3, tile.down.tile.superpositions)

        return ret

    def get_options(self, superpositions: set[int], orientation: int, tile_type: set[int]) -> list[int]:
        valid = self.collapse(superpositions, orientation, tile_type)

        ret = []

        for superposition in valid:
            if self.chance is None or superposition not in self.chance:
                ret.append(superposition)
            else:
                ret += [superposition] * self.chance[superposition]
        return ret


class Collapse(WFCAbstract):
    def __init__(self, board: Board2d[SuperpositionTile], rules: CollapseRules):
        super().__init__(board)
        self.rules = rules

    def calculate_valid_superpositions(self, tile: BoardTile[SuperpositionTile]):
        ret = []

        if tile.left:
            ret += (self.rules.get_options(tile.tile.superpositions, 0, tile.left.tile.superpositions))
        if tile.up:
            ret += (self.rules.get_options(tile.tile.superpositions, 1, tile.up.tile.superpositions))
        if tile.right:
            ret += (self.rules.get_options(tile.tile.superpositions, 2, tile.right.tile.superpositions))
        if tile.down:
            ret += (self.rules.get_options(tile.tile.superpositions, 3, tile.down.tile.superpositions))

        return ret

    def collapse_tile(self, tile: BoardTile[SuperpositionTile]):
        if not tile.tile.collapsed:
            tile.tile.superpositions = {choice(self.calculate_valid_superpositions(tile))}

    def select_tile_to_collapse(self, tiles: set[BoardTile[SuperpositionTile]]) -> BoardTile[SuperpositionTile]:
        return tiles.pop()

    def reduce_tile(self, tile: BoardTile[SuperpositionTile]):
        before = tile.tile.superpositions
        tile.tile.superpositions = self.rules.collapse_around(tile)
        return before != tile.tile.superpositions


__all__ = ['Collapse', 'CollapseRules', 'TileRules']
