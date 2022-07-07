from __future__ import annotations

from typing import Iterator


class Flood:
    def __init__(self, start_x: int, start_y: int, max_iterations: int):
        self.start_x = start_x
        self.start_y = start_y
        self.max_iterations = max_iterations

    def __iter__(self) -> "FloodIter":
        return FloodIter(self).start()


class FloodIter:
    iterator: Iterator[tuple[int, int]]

    def __init__(self, flood_info: Flood):
        self.flood_info = flood_info
        self.possible_movement = PossibleMovement()
        self.iterator = iterator((self.flood_info.start_x, self.flood_info.start_y), self.possible_movement,
                                 self.flood_info.max_iterations)

    @staticmethod
    def _box_limiter_inside(x: int, y: int, start_x: int, start_y: int, size_x: int, size_y: int) -> bool:
        return start_x <= x < start_x + size_x and start_y <= y < start_y + size_y

    @classmethod
    def box_limiter(
            cls, pos: tuple[int, int], start_x: int, start_y: int, size_x: int, size_y: int
    ) -> tuple[bool, bool, bool, bool]:
        def c(x, y): return cls._box_limiter_inside(x, y, start_x, start_y, size_x, size_y)

        return c(pos[0] - 1, pos[1]), c(pos[0], pos[1] - 1), c(pos[0] + 1, pos[1]), c(pos[0], pos[1] + 1)

    @staticmethod
    def _move_pos(pos: tuple[int, int], movement: tuple[int, int]) -> tuple[int, int]:
        return pos[0] + movement[0], pos[1] + movement[1]

    @classmethod
    def cardinal_directions(
            cls, pos: tuple[int, int]
    ) -> tuple[tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int]]:
        return cls._move_pos(pos, (-1, 0)), cls._move_pos(pos, (0, -1)), cls._move_pos(pos, (1, 0)), \
               cls._move_pos(pos, (0, 1))

    @classmethod
    def move_and(
            cls, first: tuple[bool, bool, bool, bool], second: tuple[bool, bool, bool, bool]
    ) -> tuple[bool, bool, bool, bool]:
        return first[0] and second[0], first[1] and second[1], first[2] and second[2], first[3] and second[3]

    @classmethod
    def _tile_limiter(cls, pos: tuple[int, int], tile: tuple[int, int]):
        cardinals = cls.cardinal_directions(pos)
        return cardinals[0] != tile, cardinals[1] != tile, cardinals[2] != tile, cardinals[3] != tile

    @classmethod
    def tiles_limiter(cls, pos: tuple[int, int], tiles: set[tuple[int, int]]) -> tuple[bool, bool, bool, bool]:
        current = (True, True, True, True)

        for tile in tiles:
            current = cls.move_and(current, cls._tile_limiter(pos, tile))

        return current

    def start(self):
        self.iterator = iterator((self.flood_info.start_x, self.flood_info.start_y), self.possible_movement,
                                 self.flood_info.max_iterations)
        return self

    def __iter__(self) -> "FloodIter":
        return self.start()

    def __next__(self) -> tuple[tuple[int, int], "PossibleMovement"]:
        return next(self.iterator), self.possible_movement


class PossibleMovement:
    def __init__(self):
        self.left = False
        self.up = False
        self.right = False
        self.down = False

    @staticmethod
    def _move_pos(pos: tuple[int, int], movement: tuple[int, int]) -> tuple[int, int]:
        return pos[0] + movement[0], pos[1] + movement[1]

    @classmethod
    def cardinal_directions(
            cls, pos: tuple[int, int]
    ) -> tuple[tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int]]:
        return cls._move_pos(pos, (-1, 0)), cls._move_pos(pos, (0, -1)), cls._move_pos(pos, (1, 0)), \
               cls._move_pos(pos, (0, 1))

    def get_movement(self, pos: tuple[int, int]) -> set[tuple[int, int]]:
        change: set[tuple[int, int]] = set()
        cardinals = self.cardinal_directions(pos)

        if self.left:
            change.add(cardinals[0])
        if self.up:
            change.add(cardinals[1])
        if self.right:
            change.add(cardinals[2])
        if self.down:
            change.add(cardinals[3])

        return change
    
    def all_true(self):
        self.left = True
        self.up = True
        self.right = True
        self.down = True

    def all_false(self):
        self.left = False
        self.up = False
        self.right = False
        self.down = False

    def eliminate_directions(self, left: bool, up: bool, right: bool, down: bool):
        self.left = left and self.left
        self.up = up and self.up
        self.right = right and self.right
        self.down = down and self.down


def iterator(start_pos: tuple[int, int], is_correct: PossibleMovement, max_depth: int) -> Iterator[tuple[int, int]]:
    routes: set[tuple[int, int]] = set()
    visited: set[tuple[int, int]] = set()

    def get_correct_spread(check_pos: tuple[int, int]) -> set[tuple[int, int]]:
        return is_correct.get_movement(check_pos).difference(visited)

    routes.update({start_pos})
    cnt = 0

    while len(routes):
        if cnt >= max_depth != -1:
            break
        new_routes = set()
        old_routes = set()
        for rout in routes:
            yield rout
            visited.add(rout)
            cs = get_correct_spread(rout)
            new_routes.update(cs)
            old_routes.add(rout)
        cnt += 1

        routes.update(new_routes)
        routes.difference_update(old_routes)


__all__ = ["Flood", "FloodIter", "PossibleMovement", "iterator"]
