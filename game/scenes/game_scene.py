import pygame as pg

from gamelib import BaseScene
from ..assets import tmp
from ..environment import Player


class GameScene(BaseScene):
    player: Player
    mouse_rect: pg.Rect

    def init(self):
        self.player = Player(tmp.player, pg.Vector2(500, 100))
        self.mouse_rect = pg.Rect(0, 0, 20, 20)

    def draw(self, window: pg.Surface):
        self.player.draw(window)
        pg.draw.rect(window, "red", self.mouse_rect)
        pg.draw.rect(window, "blue", self.player.rect)

    def update(self, dt: float):
        self.mouse_rect.center = pg.mouse.get_pos()
        self.player.resolve_collision(self.mouse_rect)
        self.player.update(dt)


__all__ = ["GameScene"]
