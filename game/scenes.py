import pygame as pg
from gamelib import BaseScene

from . import assets


class MainMenu(BaseScene):
    menu_text: pg.Surface
    screen_rect: pg.Rect

    def init(self):
        pg.display.set_caption("The Climb - Main menu", "The climb")
        self.menu_text = assets.title_font.render("Main Menu", True, (255, 255, 255))
        print("init")

    def after_init(self):
        self.screen_rect = self.manager.game.screen.get_rect()

    def draw(self, window: pg.Surface):
        window.fill((0, 0, 0))


__all__ = ['MainMenu']
