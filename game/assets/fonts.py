import pygame as pg
from pathlib import Path


fonts_folder = Path(__file__).parent / "fonts"
FSEX300 = str(fonts_folder / "FSEX300.ttf")
title_font = pg.font.Font(FSEX300, 32)
text_font = pg.font.Font(FSEX300, 16)


__all__ = ["title_font", "text_font"]
