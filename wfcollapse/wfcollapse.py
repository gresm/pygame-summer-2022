from abc import ABC, abstractmethod

from .board import Board2d, BoardTile
from .superposition_tile import SuperpositionTile


class WFCAbstract(ABC):
    """
    Abstract class for wave-function collapse.
    """
    @abstractmethod
    def step(self):
        """
        Perform one step of wave-function collapse.
        """
        pass

    @abstractmethod
    def collapse_tile(self, tile: BoardTile[SuperpositionTile]):
        """
        Select superposition of tile.
        """
        pass


class WFCollapse:
    """
    "WFCollapse" is Wave Function Collapse class that intends to implement wave function collapse algorithm.
    """
