from __future__ import annotations

from typing import Callable
import pygame as pg

from .gui_scene import GUIScene
from ..tools import color_iter


class TemplateGUIScene(GUIScene):
    widgets_rect: pg.Rect

    def after_init(self):
        super().after_init()
        self.widgets_rect = pg.Rect(0, 0, self.screen_rect.width - 400, 100)
        self.widgets_rect.midbottom = pg.Vector2(self.screen_rect.midbottom) - pg.Vector2(0, 50)

        self.create_location("top-left", (10, 0), "topleft", "topleft")
        self.create_location("top-right", (-10, 0), "topright", "topright")
        self.create_location("title", (0, 20), "midtop", "midtop")
        self.create_location("button-1", (50, 0), "midleft", "midleft", self.widgets_rect)
        self.create_location("button-2", (0, 0), "center", "center", self.widgets_rect)
        self.create_location("button-3", (-50, 0), "midright", "midright", self.widgets_rect)

    def draw(self, surface: pg.Surface):
        super().draw(surface)
        pg.draw.rect(surface, (255, 255, 255), self.widgets_rect, 5)


class SecondTemplate(GUIScene):
    widgets_rect: pg.Rect
    changing_bg: bool
    color_iter: Callable[[], tuple[int, int, int]]

    def init(self):
        super().init()
        self.changing_bg = True
        self.color_iter = color_iter()

    def create_locations(self):
        self.create_location("title", (0, 20), "midtop", "midtop")
        self.create_location("back", (0, 10), "midleft", "midleft")

    def setup_widget(self):
        self.widgets_rect = pg.Rect(0, 0, self.screen_rect.width - 750, self.screen_rect.height - 200)
        self.set_rect_location(self.widgets_rect, (0, 50), "title", "midtop", "midbottom")

        self.create_location("button-1", (0, 50), "midtop", "midtop", self.widgets_rect)
        self.create_location("button-2", (0, 0), "center", "center", self.widgets_rect)
        self.create_location("button-3", (0, -50), "midbottom", "midbottom", self.widgets_rect)

    def draw(self, window: pg.Surface):
        window.fill(self.color_iter())
        super().draw(window)

        pg.draw.rect(window, (255, 255, 255), self.widgets_rect, 5)


__all__ = ["TemplateGUIScene", "SecondTemplate"]
