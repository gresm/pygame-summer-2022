import pygame as pg

from gamelib import BaseScene
from ..assets import tmp
from ..environment import Player


class GameScene(BaseScene):
    player: Player

    def init(self):
        self.player = Player(tmp.player, pg.Vector2(500, 100))

    def draw(self, window: pg.Surface):
        self.player.draw(window)

    def update(self, dt: float):
        self.player.update(dt)


__all__ = ["GameScene"]
