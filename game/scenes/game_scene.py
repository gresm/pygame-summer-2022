import pygame as pg

from gamelib import BaseScene
from ..assets import tmp
from ..environment import Player
from .. import constants


class GameScene(BaseScene):
    player: Player
    mouse_rect: pg.Rect
    camera: pg.Vector2

    def init(self):
        self.player = Player(tmp.player, pg.Vector2())
        self.mouse_rect = pg.Rect(0, 0, 20, 20)
        self.camera = pg.Vector2()

    def draw(self, window: pg.Surface):
        self.player.draw(window, self.camera - constants.SCREEN_CENTER)
        pg.draw.rect(window, "white", constants.CAMERA_TOLERANCE, 5)
        pg.draw.rect(window, "red", self.mouse_rect)
        pg.draw.rect(window, "blue", self.player.rect, 5)

    def update(self, dt: float):
        self.mouse_rect.center = pg.Vector2(pg.mouse.get_pos()) + self.camera - constants.SCREEN_CENTER
        self.player.resolve_collision(self.mouse_rect)
        self.player.update(dt)

        self.camera = self.player.pos


__all__ = ["GameScene"]
