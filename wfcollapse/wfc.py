from __future__ import annotations

from .wfc_abstract import WFCAbstract


class SideGroup:
    def __init__(self, rules: CollapseRules):
        self.rules = rules
        self.id = self.rules.create_rule_id()

    def resolve(self):
        return self.id


class TileRule:
    def __init__(self, rules: CollapseRules, left: SideGroup, top: SideGroup, right: SideGroup, bottom: SideGroup):
        self.rules = rules
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom
        self._can_finalize = True
        self.cached: set[TileRule] = set()

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
        return self.create(self.left, self.top, self.right, self.bottom)

    def clone_multiple(self, number: int) -> list[TileRule]:
        ret = []
        for _ in range(number):
            ret.append(self.clone())
        return ret

    def create(self, left: SideGroup, top: SideGroup, right: SideGroup, bottom: SideGroup) -> TileRule:
        ret = TileRule(self.rules, left, top, right, bottom)
        self.cached.add(ret)
        return ret

    def flip(self, x_axis: bool, y_axis: bool) -> TileRule:
        ret = list(self.all)
        if x_axis:
            ret[0], ret[2] = ret[2], ret[0]
        if y_axis:
            ret[1], ret[3] = ret[3], ret[1]

        ret = self.create(*ret)
        return ret

    def remove(self):
        self._can_finalize = False

    def resolve_self(self):
        return self.left.resolve(), self.top.resolve(), self.right.resolve(), self.bottom.resolve()

    def resolve(self):
        ret = dict()

        if self._can_finalize:
            ret[self.rules.create_rule_id()] = self.resolve_self()

        for rule in self.cached:
            ret.update(rule.resolve())

        return ret

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

    def add_tile_rule(self, rule: TileRule):
        self.rules[self.create_rule_id()] = rule

    def create_rule_id(self) -> int:
        ret = self._rules_increment_id
        self._rules_increment_id += 1
        return ret

    def create_side_id(self) -> int:
        ret = self._side_increment_id
        self._side_increment_id += 1
        return ret

    def resolve(self):
        ret = {}

        for rule in self.rules:
            ret.update(self.rules[rule].resolve())


class Collapse:
    pass
