"""
Script for tiles in superpositions.
"""
from __future__ import annotations


class SuperpositionTile:
    def __init__(self, superpositions: set[int]):
        self.superpositions = superpositions.copy()

    @property
    def collapsed(self):
        return len(self.superpositions) == 1

    @property
    def unsolvable(self):
        return len(self.superpositions) == 0
