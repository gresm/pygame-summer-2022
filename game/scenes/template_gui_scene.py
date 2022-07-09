import pygame as pg
from .gui_scene import GUIScene


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


__all__ = ["TemplateGUIScene"]
