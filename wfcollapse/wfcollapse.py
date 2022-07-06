from abc import ABC, abstractmethod

from .board import Board2d


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
    def select_superposition(self, tile):
        """
        Select superposition of tile.
        :param tile:
        :return:
        """
        pass


class WFCollapse:
    """
    "WFCollapse" is Wave Function Collapse class that intends to implement wave function collapse algorithm.
    """

