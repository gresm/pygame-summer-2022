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

    def flip_pos(self):
        old_pos = self.pos.copy()
        self.pos = self.pos + (self.pos - self.old_pos)
        self.old_pos = old_pos

    def update(self, dt: float):
        self.flip_pos()
        self.pos = self.pos + (self.gravity * dt)
        self.sprite.step_by(int(dt))

    def draw(self, screen: pg.Surface):
        screen.blit(self.sprite.image, self.sprite.rect)


__all__ = ["Player"]
