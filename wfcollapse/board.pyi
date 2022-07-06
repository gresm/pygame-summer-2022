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

    def __init__(self, x: int, y: int, tile: _T2, board: Board2d[_T2]): ...


class Board2d(Generic[_T]):
    board: list[list[BoardTile[_T]]]
    width: int
    height: int

    def __init__(self, width: int, height: int): ...

    def get_at(self, x: int, y: int) -> _T: ...

    def set_at(self, x: int, y: int, value: _T) -> None: ...

    def tile_at(self, x: int, y: int) -> BoardTile[_T]: ...