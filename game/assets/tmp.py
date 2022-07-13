import pygame as pg

from .. import constants
from .sprites import Sprite

player_skin = pg.Surface((constants.TILE_SIZE, constants.TILE_SIZE))
player_skin.fill((255, 255, 255))
player = Sprite.deserialize(player_skin, {"default": "idle", "animations": {
    "idle": {"frames": [{"image": [0, 0, constants.TILE_SIZE, constants.TILE_SIZE]}], "speed": 1000}}})


__all__ = ["player"]
