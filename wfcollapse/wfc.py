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

    def __str__(self):
        return f'{self.left}, {self.top}, {self.right}, {self.bottom}'

    def __repr__(self):
        return str(self)

    def __getitem__(self, item):
        return (self.left, self.top, self.right, self.bottom)[item]

    @property
    def all(self):
        return self.left, self.top, self.right, self.bottom

    def flipped(self, x_axis: bool, y_axis: bool) -> TileRule:
        ret = list(self.all)
        if x_axis:
            ret[0], ret[2] = ret[2], ret[0]
        if y_axis:
            ret[1], ret[3] = ret[3], ret[1]
        return TileRule(*ret)

    def rotated(self, by: int) -> TileRule:
        def rotate(num: int, rot_by: int) -> int:
            return (num + rot_by) % 4

        ret = list(self.all)
        ret[0], ret[1], ret[2], ret[3] = ret[rotate(0, by)], ret[rotate(1, by)], ret[rotate(2, by)], ret[rotate(3, by)]
        return TileRule(*ret)


class CollapseRules:
    def __init__(self):
        self.rules = {}
        self._side_increment_id = 0
        self._rules_increment_id = 0

    def create_side_id(self) -> int:
        ret = self._side_increment_id
        self._rules_increment_id += 1
        return ret

    def create_rule_id(self) -> int:
        ret = self._rules_increment_id
        self._rules_increment_id += 1
        return ret


class Collapse:
    pass
