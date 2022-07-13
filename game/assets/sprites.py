import pygame as pg

from .spritesheet_loader import SpriteData as _SpriteData, TileData as _TileData, SpriteSheet as _SpriteSheet, \
    Animation as _Animation


class Sprite(_SpriteData, pg.sprite.Sprite):
    def __init__(self, current: str, animations: dict[str, _Animation]):
        super().__init__(current, animations)
