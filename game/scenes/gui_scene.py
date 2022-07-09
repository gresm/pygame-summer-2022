from __future__ import annotations

import pygame as pg
from gamelib import BaseScene

from .. import assets


def draw_line_under_rect(surface: pg.Surface, color: tuple[int, int, int], rect: pg.Rect):
    pg.draw.line(surface, color, rect.bottomleft, rect.bottomright)


class GUIScene(BaseScene):
    widgets: dict[str, tuple[str, int, bool]] = {}
    buttons: dict[str, tuple[pg.Surface, pg.Rect, str]]
    disabled_buttons: dict[str, tuple[pg.Surface, pg.Rect, str]]
    locations: dict[str, tuple[tuple[int, int], pg.Rect, str, str]]
    screen_rect: pg.Rect
    selected: str

    @staticmethod
    def set_rect_location(rect: pg.Rect, location: tuple[tuple[int, int], pg.Rect, str, str]):
        loc = pg.Vector2(location[0])
        container = location[1]
        anchor = location[2]
        container_anchor = location[3]

        container_anchors = {
            "midtop": container.midtop, "midbottom": container.midbottom, "midleft": container.midleft,
            "midright": container.midright, "topleft": container.topleft, "topright": container.topright,
            "bottomleft": container.bottomleft, "bottomright": container.bottomright, "center": container.center
        }

        connect_to = pg.Vector2(container_anchors[container_anchor])

        if anchor == "center":
            rect.center = connect_to + loc
        elif anchor == "topleft":
            rect.topleft = connect_to + loc
        elif anchor == "topright":
            rect.topright = connect_to + loc
        elif anchor == "bottomleft":
            rect.bottomleft = connect_to + loc
        elif anchor == "bottomright":
            rect.bottomright = connect_to + loc
        elif anchor == "midtop":
            rect.midtop = connect_to + loc
        elif anchor == "midbottom":
            rect.midbottom = connect_to + loc
        elif anchor == "midleft":
            rect.midleft = connect_to + loc
        elif anchor == "midright":
            rect.midright = connect_to + loc

    def create_button(self, name: str, text: str, location: str, is_title: bool = False):
        if is_title:
            ret = assets.title_font.render(text, True, (255, 255, 255))
        else:
            ret = assets.text_font.render(text, True, (255, 255, 255))
        ret_rect = ret.get_rect()
        self.set_rect_location(ret_rect, self.locations[location])

        self.buttons[name] = (ret, ret_rect, text)

    def create_location(
            self, name: str, position: tuple[int, int] | pg.Vector2, anchor: str = "topleft", joint: str = "topleft",
            container: pg.Rect | None = None
    ):
        if container is None:
            container = self.screen_rect
        self.locations[name] = (tuple(position), container, anchor, joint)

    def init(self):
        self.disabled_buttons = {}
        self.locations = {}
        self.buttons = {}
        self.selected = ""

    def disable_button(self, button: str):
        if button in self.buttons:
            self.disabled_buttons[button] = self.buttons[button]
            del self.buttons[button]

    def enable_button(self, button: str):
        if button in self.disabled_buttons:
            self.buttons[button] = self.disabled_buttons[button]
            del self.disabled_buttons[button]

    def toggle_button(self, button: str):
        if button in self.buttons:
            self.disable_button(button)
        else:
            self.enable_button(button)

    def after_init(self):
        self.screen_rect = self.manager.game.screen.get_rect()

    def on_event(self, event: pg.event.Event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.selected in self.buttons and self.buttons[self.selected][1].collidepoint(event.pos):
                self.option_selected(self.selected)

    def update(self, dt: float):
        self.selected = ""
        for button in self.buttons:
            if self.buttons[button][1].collidepoint(pg.mouse.get_pos()):
                self.selected = button
                break

    def draw(self, window: pg.Surface):
        for button in self.buttons:
            window.blit(self.buttons[button][0], self.buttons[button][1])
            if button == self.selected:
                draw_line_under_rect(window, (255, 255, 255), self.buttons[button][1])

    def option_selected(self, option: str):
        pass
