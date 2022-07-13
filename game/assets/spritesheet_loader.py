"""
Custom loaders for pygame-assets
Probably will be removed in the future, as pygame-assets is unmaintained

sprite_sheet.json format is as follows:
{
    "sprites": {
        "name": {
            "default": default_animation
            "animations": {
                "state": {
                    "frames": [{
                        "image": [x, y, size_x, size_y],
                        "hit-box": [x, y, size_x, size_y]
                    }, ...],
                "speed": speed
                }, ...
            }
        }, ...
    },
    "tiles": {
        "name": {
            "image": [x, y, size_x, size_y],
            "hit-box": [x, y, size_x, size_y]
        }, ...
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

_ImageWithHitBox = TypedDict("_ImageWithHitBox", {"image": _RectLike, "hit-box": _RectLike})
_ImageWithoutHitBox = TypedDict("_ImageWithoutHitBox", {"image": _RectLike})
_Image = Union[_ImageWithHitBox, _ImageWithoutHitBox]
_AnimationFrames = list[_Image]
_Animation = TypedDict("_Animation", {"frames": _AnimationFrames, "speed": int})
_Sprite = TypedDict("_Sprite", {"default": str, "animations": dict[str, _Animation]})
_Tiles = dict[str, _Image]
SheetStruct = TypedDict("SheetStruct", {"sprites": _Sprite, "tiles": _Tiles})


class ImageData:
    def __init__(self, image: pg.Surface, hit_box: pg.Rect):
        self.image = image
        self.hit_box = hit_box

    @classmethod
    def deserialize(cls, source: pg.Surface, data: _Image) -> ImageData:
        img = source.subsurface(data["image"])
        if "hit-box" in data:
            hit_box = pg.Rect(data["hit-box"])
        else:
            hit_box = img.get_bounding_rect()

        return cls(img, hit_box)


class Animation:
    def __init__(self, frames: list[ImageData], speed: int):
        self.frames = frames
        self.speed = speed
        self.current = 0

    @classmethod
    def deserialize(cls, source: pg.Surface, data: _Animation) -> Animation:
        frames = [ImageData.deserialize(source, frame) for frame in data["frames"]]
        return cls(frames, data["speed"])

    @property
    def current_image(self) -> ImageData:
        return self.frames[self.current]

    def next(self):
        self.current = (self.current + 1) % len(self.frames)


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
