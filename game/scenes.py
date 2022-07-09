import pygame as pg
from gamelib import BaseScene

from . import assets


class MainMenu(BaseScene):
    menu_text: pg.Surface
    menu_text_rect: pg.Rect
    screen_rect: pg.Rect
    widgets_rect: pg.Rect

    def init(self):
        pg.display.set_caption("The Climb - Main menu", "The climb")
        self.menu_text = assets.title_font.render("Main Menu", True, (255, 255, 255))
        self.menu_text_rect = self.menu_text.get_rect()

    def after_init(self):
        self.screen_rect = self.manager.game.screen.get_rect()
        self.widgets_rect = pg.Rect(0, 0, self.screen_rect.width - 200, 100)
        self.widgets_rect.center = pg.Vector2(self.screen_rect.midbottom) - pg.Vector2(0, 100)
        self.menu_text_rect.midbottom = pg.Vector2(self.screen_rect.midbottom) - pg.Vector2(0, 20)

    def draw(self, window: pg.Surface):
        window.fill((0, 0, 0))
        pg.draw.rect(window, (255, 0, 255), self.widgets_rect)
        window.blit(self.menu_text, self.menu_text_rect)


__all__ = ['MainMenu']
