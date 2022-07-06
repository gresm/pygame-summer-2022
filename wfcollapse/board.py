from copy import copy
from dataclasses import dataclass


@dataclass()
class BoardTile:
    x: int
    y: int
    board: "Board2d"
    tile: ...


class Board2d:
    """
    2 dimensional board with size.
    """

    def __init__(self, width, height, default_value):
        self.__width = width
        self.__height = height
        self.board = [[BoardTile(x=x, y=y, board=self, tile=copy(default_value)) for x in range(width)] for y in
                      range(height)]

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    def set_at(self, x, y, value):
        """
        Set value at position.
        """
        self.board[x][y].tile = value

    def get_at(self, x, y):
        return self.tile_at(x, y).tile

    def tile_at(self, x, y):
        return self.board[x][y]


__all__ = ["Board2d", "BoardTile"]
