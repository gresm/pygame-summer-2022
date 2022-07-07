from copy import deepcopy
from dataclasses import dataclass


@dataclass(unsafe_hash=True)
class BoardTile:
    x: int
    y: int
    board: "Board2d"
    tile: ...

    def neighbours(self):
        ret = {self.left, self.right, self.up, self.down}

        ret.discard(None)
        return ret

    @property
    def left(self):
        return self.board.tile_at(self.x - 1, self.y)

    @property
    def up(self):
        return self.board.tile_at(self.x, self.y - 1)

    @property
    def right(self):
        return self.board.tile_at(self.x + 1, self.y)

    @property
    def down(self):
        return self.board.tile_at(self.x, self.y + 1)


class Board2d:
    """
    2 dimensional board with size.
    """

    def __init__(self, width, height, default_value):
        self.__width = width
        self.__height = height
        self.board = [[BoardTile(x=x, y=y, board=self, tile=deepcopy(default_value)) for x in range(width)] for y in
                      range(height)]

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    def check_pos(self, x, y):
        """
        Check if position is in board.
        """
        return 0 <= x < self.width and 0 <= y < self.height

    def set_at(self, x, y, value):
        """
        Set value at position.
        """
        if self.check_pos(x, y):
            self.tile_at(x, y).tile = value

    def get_at(self, x, y):
        if self.check_pos(x, y):
            return self.tile_at(x, y).tile
        return None

    def tile_at(self, x, y):
        if self.check_pos(x, y):
            return self.board[y][x]
        return None


__all__ = ["Board2d", "BoardTile"]
