from __future__ import annotations

from random import choice
from typing import TypedDict
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


class TileResolveDict(TypedDict):
    sides: tuple[int, int, int, int]
    global_chance: list[int]
    neighbour_probability: list[dict[int, list[int]]]


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
        self.left_chance: dict[int, int] = {}
        self.top_chance: dict[int, int] = {}
        self.right_chance: dict[int, int] = {}
        self.bottom_chance: dict[int, int] = {}

    def __str__(self):
        return f'{self.left}, {self.top}, {self.right}, {self.bottom}'

    def __repr__(self):
        return str(self)

    def __getitem__(self, item):
        return (self.left, self.top, self.right, self.bottom)[item]

    @property
    def all(self):
        return self.left, self.top, self.right, self.bottom

    def set_neighbour_probability(self, side: int, neighbour: TileRule, chance: int):
        if side == 0:
            self.left_chance[neighbour.id] = chance
        elif side == 1:
            self.top_chance[neighbour.id] = chance
        elif side == 2:
            self.right_chance[neighbour.id] = chance
        elif side == 3:
            self.bottom_chance[neighbour.id] = chance

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

    def resolve_side_neighbour_probability(self, side: int) -> dict[int, list[int]]:
        sides = [self.left_chance, self.top_chance, self.right_chance, self.bottom_chance]
        neighbour = sides[side]
        ret = {}
        for tile_id, chance in neighbour.items():
            ret[tile_id] = [self.id] * chance
        return ret

    def resolve_self(self):
        return self.left.resolve(), self.top.resolve(), self.right.resolve(), self.bottom.resolve()

    def resolve(self) -> dict[int, TileResolveDict]:
        if self._can_finalize:
            return {self.id: {
                "sides": self.resolve_self(), "global_chance": self.global_pollute_table,
                "neighbour_probability": [
                    self.resolve_side_neighbour_probability(0),
                    self.resolve_side_neighbour_probability(1),
                    self.resolve_side_neighbour_probability(2),
                    self.resolve_side_neighbour_probability(3)
                ]
            }}
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

    def resolve(self) -> dict[int, TileResolveDict]:
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

    def _side_chance_creator(self, chances: list[int], tile: int, side_tile: int, side: int):
        if side_tile in self.rules[tile]["neighbour_probability"][side]:
            chances += self.rules[tile]["neighbour_probability"][side][side_tile]

    def get_tile_chances(self, tile_type: BoardTile[SuperpositionTile]) -> list[int]:
        ret: list[int] = []
        for tile_superpositions in tile_type.tile.superpositions:
            ret += self.rules[tile_superpositions]["global_chance"]

            for side, neighbour in enumerate(tile_type.unfiltered_neighbours()):
                if neighbour is None:
                    continue
                for super_pos in neighbour.tile.superpositions:
                    self._side_chance_creator(ret, tile_superpositions, super_pos, side)

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
