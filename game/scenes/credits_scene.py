import pygame as pg
from gamelib import BaseScene


def draw_line_under_rect(surface: pg.Surface, color: tuple[int, int, int], rect: pg.Rect):
    pg.draw.line(surface, color, rect.bottomleft, rect.bottomright)


class CreditsMenu(BaseScene):
    pass
