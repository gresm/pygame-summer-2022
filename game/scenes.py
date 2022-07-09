import pygame as pg
from gamelib import BaseScene

from . import assets


class MainMenu(BaseScene):
    def init(self):
        pg.display.set_caption("The climb - Main menu", "The climb")

    def draw(self, window: pg.Surface):
        window.fill((0, 0, 0))
        window.blit(assets.title_font.render("Main Menu", True, (255, 255, 255)), (10, 10))


__all__ = ['MainMenu']
