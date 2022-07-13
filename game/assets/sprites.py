from __future__ import annotations
import pygame as pg

from .spritesheet_loader import SpriteData as _SpriteData, TileData as _TileData, SpriteSheet as _SpriteSheet, \
    Animation as _Animation, ImageData as _ImageData


class _Positioned(pg.sprite.Sprite):
    hit_box: pg.Rect

    def __init__(self, pos: pg.Vector2 | None = None):
        super().__init__()
        self._refresh_rect = True
        self._pos = pos if pos is not None else pg.Vector2()
        self._rect = self.rect

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value: pg.Vector2):
        self._pos = value
        self._refresh_rect = True

    @property
    def rect(self) -> pg.Rect:
        if self._refresh_rect:
            self._refresh_rect = False
            rect = self.hit_box.copy()
            rect.topleft = self.pos + pg.Vector2(self.hit_box.topleft)
            self._rect = rect
            return rect
        return self._rect

    @rect.setter
    def rect(self, value: pg.Rect):
        self.pos = value.topleft
        self._refresh_rect = True

    def draw(self, screen: pg.Surface, camera: pg.Vector2 | None = None):
        if camera is None:
            screen.blit(self.image, self.rect)
        else:
            screen.blit(self.image, pg.Vector2(self.rect.topleft) - camera)


class Sprite(_SpriteData, _Positioned):
    def __init__(self, current: str, animations: dict[str, _Animation], pos: pg.Vector2 | None = None):
        super(Sprite, self).__init__(current, animations)
        super(_SpriteData, self).__init__(pos)


class Tile(_TileData, _Positioned):
    def __init__(self, image: pg.Surface, hit_box: pg.Rect, pos: pg.Vector2 | None = None):
        super(Tile, self).__init__(image, hit_box)
        super(_ImageData, self).__init__(pos)


class Sheet(_SpriteSheet):
    @classmethod
    def create_tile(cls, source: pg.Surface, data):
        return Tile.deserialize(source, data)

    @classmethod
    def create_sprite(cls, source: pg.Surface, data):
        return Sprite.deserialize(source, data)


__all__ = ["Sprite", "Tile", "Sheet"]
