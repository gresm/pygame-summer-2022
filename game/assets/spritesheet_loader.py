"""
Custom loaders for pygame-assets
Probably will be removed in the future, as pygame-assets is unmaintained

sprite_sheet.json format is as follows:
{
    "sprites": {
        "name": {
            "hit-box": [x, y, size_x, size_y],
            "frames": {
                "state": {
                    "frame": [x, y, size_x, size_y]
                },
            }
        }
    },
    "tiles": {
        "name": [x, y, size_x, size_y]
    }
}
"""
from __future__ import annotations

from pathlib import Path
from typing import TypedDict, Union
import json
import pygame as pg

sprite_sheet_folder = Path(__file__).parent / "sprite-sheet"

_RectLike = Union[tuple[int, int, int, int], list[int]]
_SheetData = TypedDict("_SheetData", {"hit-box": _RectLike, "frames": list[_RectLike]})
SheetStruct = TypedDict("SheetStruct", {"sprites": dict[str, _SheetData], "tiles": dict[str, _RectLike]})


class Sprite:
    def __init__(self, ):
        pass


class SpriteSheet:
    def __init__(self, image: pg.Surface, data: SheetStruct):
        self.image = image
        self.data = data


def load_sprite_sheet(name: str) -> SpriteSheet:
    """
    Load a sprite sheet from the asset's folder
    :param name:
    :return:
    """
    image = sprite_sheet_folder / f"{name}.png"
    config = sprite_sheet_folder / f"{name}.json"

    with config.open("r") as config_file:
        data = json.load(config_file)
    return SpriteSheet(pg.image.load(str(image)), data)


__all__ = ["load_sprite_sheet"]
