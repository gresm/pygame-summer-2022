"""
A file implementing classes for supporting infinite terrain generation (with chunks),
Using wave function collapse algorithm.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterator, Type
from copy import deepcopy

import pygame as pg

import wfcollapse as wfc


class MapTileAccess(ABC):
    """
    Abstract class for accessing map tiles.
    """

    @abstractmethod
    def get_tile(self, x: int, y: int) -> wfc.BoardTile[wfc.SuperpositionTile]:
        pass

    @abstractmethod
    def set_at(self, x: int, y: int, tile: wfc.SuperpositionTile | set[int]):
        pass

    def get_at(self, x: int, y: int) -> wfc.SuperpositionTile:
        if self.get_tile(x, y):
            return self.get_tile(x, y).tile

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


class MapChunk(MapTileAccess, ABC):
    """
    A class for representing a chunk of the map.
    """

    def __init__(self, game_map: Map, chunk: tuple[int, int], width: int, height: int,
                 default_value: wfc.SuperpositionTile):
        self.game_map = game_map
        self.chunk = chunk
        self.width = width
        self.height = height
        self.default_value = default_value
        self.board = self._create_board()
        self._collapse = self._create_collapse(self.board)

        self.reload_border()

    def __str__(self):
        return f"MapChunk(chunk={self.chunk}, width={self.width}, height={self.height})"

    def __repr__(self):
        return self.__str__()

    @abstractmethod
    def _create_collapse(self, board: wfc.Board2d[wfc.SuperpositionTile]) -> wfc.Collapse:
        pass

    @property
    def left(self):
        return self.game_map.get_chunk(self.chunk[0] - 1, self.chunk[1])

    @property
    def right(self):
        return self.game_map.get_chunk(self.chunk[0] + 1, self.chunk[1])

    @property
    def up(self):
        return self.game_map.get_chunk(self.chunk[0], self.chunk[1] - 1)

    @property
    def down(self):
        return self.game_map.get_chunk(self.chunk[0], self.chunk[1] + 1)

    def _create_board(self) -> wfc.Board2d[wfc.SuperpositionTile]:
        return wfc.Board2d(self.width, self.height, self.default_value)

    def collapse(self):
        self._collapse.collapse()

    def get_tile(self, x: int, y: int) -> wfc.BoardTile[wfc.SuperpositionTile]:
        return self.board.tile_at(x, y)

    def get_tile_border_side(self, x: int, y: int) -> set[int]:
        """
        Get the side of the tile border that is closest to the given tile.
        """
        ret = set()
        if x == 0:
            ret.add(1)
        elif y == 0:
            ret.add(2)
        elif x == self.width - 1:
            ret.add(3)
        elif y == self.height - 1:
            ret.add(4)
        return ret

    def refresh_tile(self, x: int, y: int):
        self.set_at(x, y, self.get_at(x, y))

    def reload_border(self):
        for i in range(self.width):
            self.refresh_tile(i, 0)
            self.refresh_tile(i, self.height - 1)

        for i in range(self.height):
            self.refresh_tile(0, i)
            self.refresh_tile(self.width - 1, i)

    def set_at(self, x: int, y: int, tile: wfc.SuperpositionTile | set[int]):
        if isinstance(tile, set):
            self.board.set_at(x, y, wfc.SuperpositionTile(tile))
        else:
            self.board.set_at(x, y, deepcopy(tile))
        if self.board.tile_at(x, y):
            self._collapse.wave_tile(self.board.tile_at(x, y))

        tile_border = self.get_tile_border_side(x, y)

        if 1 in tile_border and self.left:
            self.left.set_at(self.width - 1, y, tile)
        if 2 in tile_border and self.up:
            self.up.set_at(x, self.height - 1, tile)
        if 3 in tile_border and self.right:
            self.right.set_at(0, y, tile)
        if 4 in tile_border and self.down:
            self.down.set_at(x, 0, tile)


class Map(MapTileAccess):
    def __init__(self, chunk_width: int, chunk_height: int, default_value: wfc.SuperpositionTile,
                 chunk_type: Type[MapChunk]):
        self.chunk_width = chunk_width
        self.chunk_height = chunk_height
        self.map: dict[tuple[int, int], MapChunk] = {}
        self.default_value = default_value
        self.chunk_type = chunk_type

    def spawn_chunk(self, chunk_x: int, chunk_y: int):
        self.map[chunk_x, chunk_y] = self.chunk_type(self, (chunk_x, chunk_y), self.chunk_width, self.chunk_height,
                                                     self.default_value)

    def calculate_pos(self, x: int, y: int) -> tuple[int, int, int, int]:
        local_x = x % self.chunk_width
        local_y = y % self.chunk_height
        chunk_x = (x - local_x) // self.chunk_width
        chunk_y = (y - local_y) // self.chunk_height
        return chunk_x, chunk_y, local_x, local_y

    def get_chunk(self, chunk_x: int, chunk_y: int) -> MapChunk | None:
        if (chunk_x, chunk_y) in self.map:
            return self.map[(chunk_x, chunk_y)]

    def get_tile(self, x: int, y: int) -> wfc.BoardTile[wfc.SuperpositionTile]:
        local_x, local_y, chunk_x, chunk_y = self.calculate_pos(x, y)

        if (chunk_x, chunk_y) not in self.map:
            self.spawn_chunk(chunk_x, chunk_y)
        return self.map[(chunk_x, chunk_y)].get_tile(local_x, local_y)

    def set_at(self, x: int, y: int, tile: wfc.SuperpositionTile | set[int]):
        local_x, local_y, chunk_x, chunk_y = self.calculate_pos(x, y)
        if (chunk_x, chunk_y) not in self.map:
            self.spawn_chunk(chunk_x, chunk_y)
        self.map[(chunk_x, chunk_y)].set_at(local_x, local_y, tile)
