"""
Script for tiles in superpositions.
"""
from __future__ import annotations


class SuperpositionTile:
    def __init__(self, superpositions):
        self.superpositions = superpositions.copy()

    @staticmethod
    def least_entropy_tiles(board):
        """
        Returns tiles with the least entropy.
        """
        ret = set()
        least_entropy = -1
        for line in board.board:
            for tile in line:
                if tile.tile.collapsed:
                    continue
                if least_entropy == -1 or least_entropy == tile.tile.entropy():
                    least_entropy = tile.tile.entropy()
                    ret.add(tile)
                elif least_entropy > tile.tile.entropy():
                    least_entropy = tile.tile.entropy()
                    ret = {tile}
        return ret

    @property
    def collapsed(self):
        return self.entropy() <= 1

    @property
    def unsolvable(self):
        return self.entropy() == 0

    def entropy(self):
        return len(self.superpositions)


__all__ = ["SuperpositionTile"]
