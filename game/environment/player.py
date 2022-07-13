from __future__ import annotations

import pygame as pg
from ..assets.sprites import Sprite


class Player:
    """
    Implement a player in the game using Verlet's integration.
    """
    def __init__(self, sprite: Sprite, pos: pg.Vector2):
        self.sprite = sprite
        self.pos = pos
        self.old_pos = self.pos.copy()
        self.gravity = pg.Vector2(0, 10)

    @property
    def pos(self) -> pg.Vector2:
        return self.sprite.pos

    @pos.setter
    def pos(self, value: pg.Vector2):
        self.sprite.pos = value

    @property
    def rect(self):
        return self.sprite.rect

    @rect.setter
    def rect(self, value: pg.Rect):
        self.sprite.rect = value

    def flip_pos(self):
        old_pos = self.pos.copy()
        self.pos = self.pos + (self.pos - self.old_pos)
        self.old_pos = old_pos

    def update(self, dt: float):
        self.flip_pos()
        self.pos = self.pos + (self.gravity * dt)
        self.sprite.step_by(int(dt))

    def draw(self, screen: pg.Surface, camera: pg.Vector2 | None = None):
        self.sprite.draw(screen, camera)

    def resolve_collision(self, other: pg.Rect) -> tuple[bool, int]:
        if not self.rect.colliderect(other):
            return False, -1

        left_fix = other.left - self.rect.right + 1
        right_fix = self.rect.left - other.right - 1
        top_fix = other.top - self.rect.bottom + 1
        bottom_fix = self.rect.top - other.bottom - 1
        fix = min((left_fix, 0), (top_fix, 1), (right_fix, 2), (bottom_fix, 3), key=lambda x: abs(x[0]))
        if fix[1] == 0:
            self.pos.x += fix[0]
        elif fix[1] == 1:
            self.pos.y += fix[0]
        elif fix[1] == 2:
            self.pos.x -= fix[0]
        elif fix[1] == 3:
            self.pos.y -= fix[0]

        return True, fix[1]


__all__ = ["Player"]
