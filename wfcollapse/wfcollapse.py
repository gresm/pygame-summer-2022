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
    def solve_tile(self, tile: BoardTile[SuperpositionTile]):
        """
        Reduce superpositions of the tile.
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

    def find_tile_to_collapse(self) -> BoardTile[SuperpositionTile] | None:
        """
        Select a tile to collapse.
        """
        entropies = SuperpositionTile.least_entropy_tiles(self.board)
        if len(entropies) == 0:
            return None
        return self.select_tile_to_collapse(entropies)
    
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
                collapsable_neighbours[2] = True

        if self.board.check_pos(tile.x, tile.y - 1):
            t = self.board.tile_at(tile.x, tile.y - 1)
            if not t.tile.collapsed:
                collapsable_neighbours[1] = True

        if self.board.check_pos(tile.x, tile.y + 1):
            t = self.board.tile_at(tile.x, tile.y + 1)
            if not t.tile.collapsed:
                collapsable_neighbours[3] = True

        return collapsable_neighbours

    def wave_tile(self, tile: BoardTile[SuperpositionTile]):

        flood = FloodIter(Flood(self.wave_depths, self.board.width, self.board.height))
        for pos, move in flood:
            current_tile = self.board.tile_at(pos[0], pos[1])
            if pos[0] != tile.x and pos[1] != tile.y:
                self.solve_tile(current_tile)

            move.all_true()
            move.eliminate_directions(*self.get_collapsable_neighbours(current_tile))
            move.eliminate_directions(*flood.box_limiter(pos, 0, 0, self.board.width, self.board.height))

    def step(self):
        """
        Perform one step of wave-function collapse.
        Returns False to stop the algorithm.
        """
        tile = self.find_tile_to_collapse()
        if tile is None:
            return False

        self.collapse_tile(tile)
        self.wave_tile(tile)

        return True

    def solve(self):
        """
        Solve the wave-function collapse.
        """
        while self.step():
            yield self.board
