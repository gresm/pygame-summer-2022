from __future__ import annotations

from random import choice
from .board import Board2d, BoardTile
from .superposition_tile import SuperpositionTile
from .wfc_abstract import WFCAbstract


class SideGroup:
    def __init__(self, rules: CollapseRules):
        self.rules = rules
        self.id = self.rules.create_side_id()

    def __str__(self):
        return f"<{self.__class__.__module__}.{self.__class__.__name__}(id={self.id})>"

    def resolve(self):
        return self.id


class TileRule:
    def __init__(self, rules: CollapseRules, left: SideGroup, top: SideGroup, right: SideGroup, bottom: SideGroup,
                 global_chance: int = 1):
        self.rules = rules
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom
        self._can_finalize = True
        self.global_chance = global_chance
        self.id = self.rules.add_tile_rule(self)
        self.global_pollute_table = [self.id] * self.global_chance

    def __str__(self):
        return f'{self.left}, {self.top}, {self.right}, {self.bottom}'

    def __repr__(self):
        return str(self)

    def __getitem__(self, item):
        return (self.left, self.top, self.right, self.bottom)[item]

    @property
    def all(self):
        return self.left, self.top, self.right, self.bottom

    def clone(self) -> TileRule:
        ret = self.create(self.left, self.top, self.right, self.bottom)
        return ret

    def clone_multiple(self, number: int) -> list[TileRule]:
        ret = []
        for _ in range(number):
            ret.append(self.clone())
        return ret

    def create(self, left: SideGroup, top: SideGroup, right: SideGroup, bottom: SideGroup) -> TileRule:
        ret = TileRule(self.rules, left, top, right, bottom)
        return ret

    def flip(self, x_axis: bool = False, y_axis: bool = False) -> TileRule:
        ret = list(self.all)
        print(ret)
        if x_axis:
            ret[0], ret[2] = ret[2], ret[0]
        if y_axis:
            ret[1], ret[3] = ret[3], ret[1]

        print(ret)
        ret = self.create(*ret)
        return ret

    def remove(self):
        self._can_finalize = False

    def resolve_self(self):
        return self.left.resolve(), self.top.resolve(), self.right.resolve(), self.bottom.resolve()

    def resolve(self) -> dict[int, dict[str, tuple[int, int, int, int] | list[int]]]:
        if self._can_finalize:
            return {self.id: {"sides": self.resolve_self(), "global-chance": self.global_pollute_table}}
        return {}

    def rotate(self, by: int) -> TileRule:
        def rotate(num: int, rot_by: int) -> int:
            return (num + rot_by) % 4

        ret = list(self.all)
        ret[0], ret[1], ret[2], ret[3] = ret[rotate(0, by)], ret[rotate(1, by)], ret[rotate(2, by)], ret[rotate(3, by)]
        ret = self.create(*ret)
        return ret

    def rotate_multiple(self, by: int, number: int):
        ret = []

        for inc in range(number):
            ret.append(self.rotate(by * inc))

        return ret


class CollapseRules:
    def __init__(self):
        self.rules: dict[int, TileRule] = {}
        self._side_increment_id = 0
        self._rules_increment_id = 0

    def add(self, *tiles: TileRule):
        """
        Pretend to add list of tiles to the rules, in reality do nothing.
        """
        pass

    def add_tile_rule(self, rule: TileRule) -> int:
        rule_id = self.create_rule_id()
        self.rules[rule_id] = rule
        return rule_id

    def create_rule_id(self) -> int:
        ret = self._rules_increment_id
        self._rules_increment_id += 1
        return ret

    def create_side_id(self) -> int:
        ret = self._side_increment_id
        self._side_increment_id += 1
        return ret

    def resolve(self) -> dict[int, dict[str, tuple[int, int, int, int] | list[int]]]:
        ret = {}

        for rule in self.rules:
            ret.update(self.rules[rule].resolve())

        return ret


class Collapse(WFCAbstract):
    def __init__(self, board: Board2d[SuperpositionTile], rules: CollapseRules):
        super().__init__(board)
        self.rules = rules.resolve()

    @staticmethod
    def _opposite_side(side: int) -> int:
        return (side + 2) % 4

    def _reduce_tile_by_side(self, tile: BoardTile[SuperpositionTile], side: int) -> set[int]:
        compare_with = tile.neighbour_by_side(side)
        if compare_with is None or compare_with.tile.unsolvable:
            return tile.tile.superpositions
        compare_side = self._opposite_side(side)

        to_keep: set[int] = set()

        for superposition in tile.tile.superpositions:
            for opposed_superposition in compare_with.tile.superpositions:
                if self.rules[superposition]["sides"][side] == self.rules[opposed_superposition]["sides"][compare_side]:
                    to_keep.add(superposition)

        return to_keep

    def get_tile_chances(self, tile_type: BoardTile[SuperpositionTile]) -> list[int]:
        ret: list[int] = []
        for tile_superpositions in tile_type.tile.superpositions:
            ret += self.rules[tile_superpositions]["global-chance"]

        return ret

    def collapse_tile(self, tile: BoardTile[SuperpositionTile]):
        if not tile.tile.collapsed:
            self.reduce_tile(tile)
            tile.tile.superpositions = {choice(self.get_tile_chances(tile))}

    def reduce_tile(self, tile: BoardTile[SuperpositionTile]):
        for side in range(4):
            tile.tile.superpositions = self._reduce_tile_by_side(tile, side)

    def select_tile_to_collapse(self, tiles: set[BoardTile[SuperpositionTile]]) -> BoardTile[SuperpositionTile]:
        return choice(list(tiles))
