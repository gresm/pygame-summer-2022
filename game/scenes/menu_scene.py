from __future__ import annotations

import webbrowser
import pygame as pg
from gamelib import BaseScene

from .. import assets

from .quit_scene import QuitScene
from .gui_scene import GUIScene


def draw_line_under_rect(surface: pg.Surface, color: tuple[int, int, int], rect: pg.Rect):
    pg.draw.line(surface, color, rect.bottomleft, rect.bottomright)


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


class MainMenu(TemplateGUIScene):
    def after_init(self):
        super().after_init()

        self.create_button("title", "Main Menu", "title", is_title=True)
        self.create_button("new-game", "New Game", "button-1")
        self.create_button("options", "Options", "button-2")
        self.create_button("quit", "Quit", "button-3")

    def option_selected(self, option: str):
        if option == "new-game":
            print("New Game")
        elif option == "options":
            print("options")
        elif option == "quit":
            print("quit")

    def draw(self, window: pg.Surface):
        super().draw(window)


__all__ = ["MainMenu", TemplateGUIScene]
