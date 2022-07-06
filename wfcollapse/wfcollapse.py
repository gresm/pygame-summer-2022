from __future__ import annotations

from abc import ABC, abstractmethod
from .board import Board2d, BoardTile
from .superposition_tile import SuperpositionTile


class WFCAbstract(ABC):
    """
    Abstract class for wave-function collapse.
    """
    def __init__(self, board: Board2d[SuperpositionTile]):
        self.board = board

    @abstractmethod
    def solve_tile(self, tile: BoardTile[SuperpositionTile]):
        """
        Reduce superpositions of the tile, if all superpositions reduced to 1, return True, else False.
        """
        pass

    @abstractmethod
    def collapse_tile(self, tile: BoardTile[SuperpositionTile]):
        """
        Collapse a tile to one superposition.
        """
        pass

    @abstractmethod
    def select_tile_to_collapse(self, tiles: set[BoardTile[SuperpositionTile]]):
        """
        Select a tile to collapse.
        """
        pass

    def find_tile_to_collapse(self):
        """
        Select a tile to collapse.
        """
        return self.select_tile_to_collapse(SuperpositionTile.least_entropy_tiles(self.board))

    def step(self):
        """
        Perform one step of wave-function collapse.
        """
        pass


class WFCollapse:
    """
    "WFCollapse" is Wave Function Collapse class that intends to implement wave function collapse algorithm.
    """
