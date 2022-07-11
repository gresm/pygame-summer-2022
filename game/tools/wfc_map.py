"""
A file implementing classes for supporting infinite terrain generation (with chunks) using wave function collapse algorithm.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterator
import pygame as pg
import wfcollapse as wfc


class MapTileAccess(ABC):
    """
    Abstract class for accessing map tiles.
    """

    @abstractmethod
    def get_tile(self, x, y) -> wfc.BoardTile[wfc.SuperpositionTile]:
        pass

    def get_tiles(self, rect: pg.Rect) -> Iterator[wfc.BoardTile[wfc.SuperpositionTile]]:
        for x in range(rect.left, rect.right):
            for y in range(rect.top, rect.bottom):
                yield self.get_tile(x, y)

    def get_similar_neighbours(
            self, tile: wfc.BoardTile[wfc.SuperpositionTile], superposition: int, max_steps: int = 10
    ) -> Iterator[wfc.BoardTile[wfc.SuperpositionTile]]:
        """
        Get all tiles that are similar to the given tile using flood iter.
        """
        flood_settings = wfc.Flood(tile.x, tile.y, max_steps)
        flood = wfc.FloodIter(flood_settings)
        for pos, move in flood:
            move.all_true()
            if superposition not in self.get_tile(pos[0], pos[1]).tile.superpositions:
                move.all_false()
                continue
            yield self.get_tile(pos[0], pos[1])


class MapChunk(MapTileAccess):
    """
    A class for representing a chunk of the map.
    """

    def __init__(self, chunk: tuple[int, int], width: int, height: int, board: wfc.Board2d[wfc.SuperpositionTile]):
        self.chunk = chunk
        self.width = width
        self.height = height
        self.board = board

    def __str__(self):
        return f"MapChunk(chunk={self.chunk}, width={self.width}, height={self.height})"

    def __repr__(self):
        return self.__str__()

    def get_tile(self, x, y) -> wfc.BoardTile[wfc.SuperpositionTile]:
        return self.board.tile_at(x, y)
