from __future__ import annotations

from random import choice
from .wfcollapse import WFCAbstract
from .board import Board2d, BoardTile
from .superposition_tile import SuperpositionTile


class TileRules:
    def __init__(self, rules: tuple[set[int], set[int], set[int], set[int]]):
        self.rules = rules

    @classmethod
    def parse(cls, rules: list[list[int]]):
        return cls(
            (
                set(rules[0]),
                set(rules[1]),
                set(rules[2]),
                set(rules[3])
            )
        )

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

    @classmethod
    def parse(cls, rules: list[list[list[int]]]):
        rules_dict = {}
        for superposition in range(len(rules)):
            rules_dict[superposition] = TileRules.parse(rules[superposition])
        return cls(rules_dict)

    def collapse(self, superpositions: set[int], orientation: int, tile_type: set[int]):
        if not len(tile_type):
            return superpositions

        valid: set[int] = set()

        for superposition in superpositions:
            for tile_type in tile_type:
                if self.rules[superposition].compare(orientation, tile_type):
                    valid.add(superposition)
        return valid

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

        ret += (self.rules.get_options(tile.tile.superpositions, 0, tile.left.tile.superpositions))
        ret += (self.rules.get_options(tile.tile.superpositions, 1, tile.up.tile.superpositions))
        ret += (self.rules.get_options(tile.tile.superpositions, 2, tile.right.tile.superpositions))
        ret += (self.rules.get_options(tile.tile.superpositions, 3, tile.down.tile.superpositions))

        return ret

    def collapse_tile(self, tile: BoardTile[SuperpositionTile]):
        if not tile.tile.collapsed:
            tile.tile.superpositions = {choice(self.calculate_valid_superpositions(tile))}

    def select_tile_to_collapse(self, tiles: set[BoardTile[SuperpositionTile]]) -> BoardTile[SuperpositionTile]:
        return tiles.pop()


__all__ = ['Collapse']
