# Stub file for "superposition_tile.py".
from __future__ import annotations

from .board import Board2d, BoardTile

class SuperpositionTile:
    superpositions: set[int]
    collapsed: bool
    unsolvable: bool

    def __init__(self, superpositions: set[int]): ...

    @staticmethod
    def least_entropy_tiles(board: Board2d[SuperpositionTile]) -> set[BoardTile[SuperpositionTile]]: ...

    def entropy(self) -> int: ...