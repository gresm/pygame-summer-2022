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
    def reduce_tile(self, tile: BoardTile[SuperpositionTile]) -> bool:
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

        flood = FloodIter(Flood(tile.x, tile.y, self.wave_depths))
        for pos, move in flood:
            yield pos

            move.all_true()
            current_tile = self.board.tile_at(pos[0], pos[1])
            move.eliminate_directions(*self.get_collapsable_neighbours(current_tile))
            move.eliminate_directions(*flood.box_limiter(pos, 0, 0, self.board.width, self.board.height))

            if pos[0] != tile.x and pos[1] != tile.y:
                if not self.reduce_tile(current_tile):
                    move.all_false()

    def set_tile(self, pos: tuple[int, int], superpositions: set[int]):
        if self.board.tile_at(pos[0], pos[1]):
            self.board.tile_at(pos[0], pos[1]).tile.superpositions = superpositions.copy()
            self.wave_tile(self.board.tile_at(pos[0], pos[1]))

    def step(self):
        """
        Perform one step of wave-function collapse.
        Returns False to stop the algorithm.
        """
        tile = self.find_tile_to_collapse()
        if tile is None:
            return False

        self.reduce_tile(tile)
        self.collapse_tile(tile)
        return self.wave_tile(tile)

    def solve(self):
        """
        Solve the wave-function collapse.
        """
        while True:
            step = self.step()
            if not step:
                break
            yield step

    def collapse(self):
        """
        Collapse the board.
        """
        for step in self.solve():
            for _ in step:
                pass
