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

    def start(self):
        self.iterator = iterator((self.flood_info.start_x, self.flood_info.start_y), self.possible_movement,
                                 self.flood_info.max_iterations)
        return self

    def __iter__(self) -> "FloodIter":
        return self.start()

    def __next__(self) -> tuple[int, int, "PossibleMovement"]:
        return next(self.iterator) + (self.possible_movement, )


class PossibleMovement:
    def __init__(self):
        self.left = False
        self.up = False
        self.right = False
        self.down = False
    
    @staticmethod
    def _move_pos(pos: tuple[int, int], movement: tuple[int, int]) -> tuple[int, int]:
        return pos[0] + movement[0], pos[1] + movement[1]

    def get_movement(self, pos: tuple[int, int]) -> set[tuple[int, int]]:
        change: set[tuple[int, int]] = set()

        if self.left:
            change.add((-1, 0))
        if self.up:
            change.add((0, -1))
        if self.right:
            change.add((1, 0))
        if self.down:
            change.add((0, 1))

        return {self._move_pos(pos, movement) for movement in change}
    
    def all_true(self):
        self.left = True
        self.up = True
        self.up = True
        self.down = True
    
    def all_false(self):
        self.left = False
        self.up = False
        self.up = False
        self.down = False


def iterator(start_pos: tuple[int, int], is_correct: PossibleMovement, max_depth: int) -> Iterator[tuple[int, int]]:
    routes: set[tuple[int, int]] = set()
    visited: set[tuple[int, int]] = set()

    def get_correct_spread(check_pos: tuple[int, int]) -> set[tuple[int, int]]:
        return is_correct.get_movement(check_pos).difference(visited)

    routes.update(get_correct_spread(start_pos))
    cnt = 0

    while len(routes):
        if cnt >= max_depth != -1:
            break
        new_routes = set()
        old_routes = set()
        for rout in routes:
            visited.add(rout)
            new_routes.update(get_correct_spread(rout))
            old_routes.add(rout)
            yield rout
        cnt += 1

        routes.update(new_routes)
        routes.difference_update(old_routes)


__all__ = ["Flood", "FloodIter", "PossibleMovement", "iterator"]
