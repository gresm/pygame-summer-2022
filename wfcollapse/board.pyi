# Python stub file for "board.py"
from __future__ import annotations


from typing import TypeVar, Generic
from dataclasses import dataclass


_T = TypeVar("_T")
_T2 = TypeVar("_T2")


@dataclass()
class BoardTile(Generic[_T2]):
    x: int
    y: int
    tile: _T2
    board: Board2d[_T2]
    left: BoardTile[_T2] | None
    right: BoardTile[_T2] | None
    up: BoardTile[_T2] | None
    down: BoardTile[_T2] | None

    def __init__(self, x: int, y: int, tile: _T2, board: Board2d[_T2]): ...

    def neighbours(self) -> set[BoardTile[_T2]]: ...

    def neighbour_by_side(self, side: int) -> BoardTile[_T2]: ...


class Board2d(Generic[_T]):
    board: list[list[BoardTile[_T]]]
    width: int
    height: int

    def __init__(self, width: int, height: int, default_value: object): ...

    def check_pos(self, x: int, y: int) -> bool: ...

    def get_at(self, x: int, y: int) -> _T | None: ...

    def set_at(self, x: int, y: int, value: _T) -> None: ...

    def tile_at(self, x: int, y: int) -> BoardTile[_T] | None: ...