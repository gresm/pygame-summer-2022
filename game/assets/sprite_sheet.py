# sprite_sheet.py
from .spritesheet_loader import load_sprite_sheet


tiles_sheet = load_sprite_sheet("tiles")

__all__ = ["tiles_sheet"]
