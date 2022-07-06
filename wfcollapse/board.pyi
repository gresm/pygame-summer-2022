# Python stub file for "board.py"
from __future__ import annotations

from typing import TypeVar, Generic

_T = TypeVar("_T")

class Board2d(Generic[_T]):
    board: list[list[_T]]
    width: int
    height: int

    def __init__(self, width: int, height: int): ...
    def get_at(self, x: int, y: int) -> _T: ...
    def set_at(self, x: int, y: int, value: _T) -> None: ...