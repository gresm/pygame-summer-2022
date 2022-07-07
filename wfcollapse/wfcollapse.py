from __future__ import annotations

from abc import ABC, abstractmethod
from .board import Board2d, BoardTile
from .superposition_tile import SuperpositionTile
from .flood_iter import FloodIter, Flood


class WFCAbstract(ABC):
    wave_depths: int = -1
    
    """
    Abstract class for wave-function collapse.
    """
    def __init__(self, board: Board2d[SuperpositionTile]):
        self.board = board

    @abstractmethod
    def solve_tile(self, tile: BoardTile[SuperpositionTile]) -> bool:
        """
        Reduce superpositions of the tile, if none of superpositions will be reduced return false, true otherwise.
        """
        pass

    @abstractmethod
    def collapse_tile(self, tile: BoardTile[SuperpositionTile]):
        """
        Collapse a tile to one superposition.
        """
        pass

    @abstractmethod
    def select_tile_to_collapse(self, tiles: set[BoardTile[SuperpositionTile]]) -> BoardTile[SuperpositionTile]:
        """
        Select a tile to collapse.
        """
        pass

    def find_tile_to_collapse(self) -> BoardTile[SuperpositionTile]:
        """
        Select a tile to collapse.
        """
        return self.select_tile_to_collapse(SuperpositionTile.least_entropy_tiles(self.board))
    
    def get_collapsable_neighbours(self, tile: BoardTile[SuperpositionTile]):
        """
        Get all tiles that can be collapsed.
        """
        collapsable_neighbours = [False, False, False, False]

        if self.board.check_pos(tile.x - 1, tile.y):
            t = self.board.tile_at(tile.x - 1, tile.y)
            if not t.tile.collapsed:
                collapsable_neighbours[0] = True

        if self.board.check_pos(tile.x + 1, tile.y):
            t = self.board.tile_at(tile.x + 1, tile.y)
            if not t.tile.collapsed:
                collapsable_neighbours[1] = True

        if self.board.check_pos(tile.x, tile.y - 1):
            t = self.board.tile_at(tile.x, tile.y - 1)
            if not t.tile.collapsed:
                collapsable_neighbours[2] = True

        if self.board.check_pos(tile.x, tile.y + 1):
            t = self.board.tile_at(tile.x, tile.y + 1)
            if not t.tile.collapsed:
                collapsable_neighbours[3] = True

        return collapsable_neighbours

    def step(self):
        """
        Perform one step of wave-function collapse.
        """
        tile = self.find_tile_to_collapse()
        if tile is None:
            return False
        if self.solve_tile(tile):
            self.collapse_tile(tile)
            return True
        return False


class WFCollapse:
    """
    "WFCollapse" is Wave Function Collapse class that intends to implement wave function collapse algorithm.
    """
