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
SheetStruct = TypedDict("SheetStruct", {"sprites": dict[str, _Sprite], "tiles": _Tiles})


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

    def step_by(self, inc: int):
        self.current = (self.current + inc) % len(self.frames)


class SpriteData:
    def __init__(self, current: str, animations: dict[str, Animation]):
        self._current = current
        self.animations = animations
        self.anim_cnt = 0

    @classmethod
    def deserialize(cls, source: pg.Surface, data: _Sprite) -> SpriteData:
        animations = {
            name: Animation.deserialize(source, anim)
            for name, anim in data["animations"].items()
        }
        return cls(data["default"], animations)

    @property
    def current_animation(self) -> Animation:
        return self.animations[self._current]

    @property
    def image(self) -> ImageData:
        return self.current_animation.current_image

    def step_by(self, inc: int):
        self.anim_cnt += inc
        fixed = self.anim_cnt % self.current_animation.speed
        steps = (self.anim_cnt - fixed) // self.current_animation.speed
        self.anim_cnt = fixed
        self.current_animation.step_by(steps)


class TileData(ImageData):
    pass


class SpriteSheet:
    def __init__(self, image: pg.Surface, sprites: dict[str, SpriteData], tiles: dict[str, TileData]):
        self.image = image
        self.sprites = sprites
        self.tiles = tiles

    @classmethod
    def deserialize(cls, source: pg.Surface, data: SheetStruct) -> SpriteSheet:
        sprites = {
            name: cls.create_sprite(source, data["sprites"][name])
            for name, sprite in data["sprites"].items()
        }
        tiles = {
            name: cls.create_tile(source, tile)
            for name, tile in data["tiles"].items()
        }
        return cls(source, sprites, tiles)

    @classmethod
    def create_sprite(cls, source: pg.Surface, data: _Sprite):
        return SpriteData.deserialize(source, data)

    @classmethod
    def create_tile(cls, source: pg.Surface, data: _Image):
        return TileData.deserialize(source, data)


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
    return SpriteSheet.deserialize(pg.image.load(str(image)), data)


def load_grid_map(name: str, tile_width: int, tile_height: int) -> list[list[pg.Surface]]:
    """
    Load a grid map from the asset's folder
    """
    image_file = sprite_sheet_folder / f"{name}.png"
    image = pg.image.load(str(image_file))
    ret = []

    for x in range(0, image.get_width(), tile_width):
        ret.append([])
        for y in range(0, image.get_height(), tile_height):
            ret[-1].append(image.subsurface(pg.Rect(x, y, tile_width, tile_height)))
    return ret


__all__ = ["load_sprite_sheet", "load_grid_map", "SpriteSheet", "SpriteData", "TileData", "SheetStruct", "Animation"]
