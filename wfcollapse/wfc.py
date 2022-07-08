from __future__ import annotations

from typing import Iterable, Union
from random import choice
from .wfcollapse import WFCAbstract
from .board import Board2d, BoardTile
from .superposition_tile import SuperpositionTile

_TileSideFormat = Union[Iterable[int], int, None]

_TileRulesFormat = tuple[
    _TileSideFormat,  # left
    _TileSideFormat,  # top
    _TileSideFormat,  # right
    _TileSideFormat,  # bottom
]


class TileRules:
    def __init__(self, rules: tuple[set[int], set[int], set[int], set[int]]):
        self.rules = rules

    @classmethod
    def parse(
            cls, rules: _TileRulesFormat
    ) -> TileRules:
        def transform(side: _TileSideFormat) -> set[int]:
            if side is None:
                return set()
            if isinstance(side, int):
                return {side}
            return set(side)
    
        return cls((transform(rules[0]), transform(rules[1]), transform(rules[2]), transform(rules[3])))

    def compare(self, orientation: int, tile_type: int) -> bool:
        if not 0 <= orientation < 4:
            return False

        if tile_type == -1 or len(self.rules[orientation]) == 0:
            return True

        return tile_type in self.rules[orientation]


class CollapseRules:
    def __init__(self, rules: dict[int, TileRules], chance: dict[int, int] | None = None):
        self.rules = rules
        self.chance = chance
        self._fix_rules()

    @classmethod
    def parse(cls, rules: dict[int, _TileRulesFormat], chance: list[int] | None = None):
        rules_dict = {r: TileRules.parse(rules[r]) for r in rules}
        return cls(rules_dict, {i: chance[i] for i in range(len(chance))} if chance else None)

    def _fix_rules(self):
        for superposition in self.rules:
            left_rule = self.rules[superposition].rules[0]
            top_rule = self.rules[superposition].rules[1]
            right_rule = self.rules[superposition].rules[2]
            bottom_rule = self.rules[superposition].rules[3]

            for allowed in left_rule:
                self.rules[allowed].rules[2].add(superposition)

            for allowed in top_rule:
                self.rules[allowed].rules[3].add(superposition)

            for allowed in right_rule:
                self.rules[allowed].rules[0].add(superposition)

            for allowed in bottom_rule:
                self.rules[allowed].rules[1].add(superposition)

    def collapse(self, superpositions: set[int], orientation: int, tile_type: set[int]):
        if not len(tile_type):
            return superpositions

        valid: set[int] = set()

        for superposition in superpositions:
            for tile in tile_type:
                if self.rules[superposition].compare(orientation, tile):
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

    def solve_tile(self, tile: BoardTile[SuperpositionTile]):
        before = tile.tile.superpositions
        tile.tile.superpositions = self.rules.collapse_around(tile)
        return before != tile.tile.superpositions


__all__ = ['Collapse', 'CollapseRules', 'TileRules']
