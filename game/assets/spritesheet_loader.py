"""
Custom loaders for pygame-assets
Probably will be removed in the future, as pygame-assets is unmaintained

sprite_sheet.json format is as follows:
{
    "normal": [x, y, width, height],
    "scaled": [x, y, width, height, scale],
    "tiled": [x, y, width, height, tile_width, tile_height],
    "tiled_and_scaled": [x, y, width, height, tile_width, tile_height, scale]
}

Where:
    x, y, width, height: coordinates and size of the sprite as int
    scale: scale of the sprite as float
    tile_width, tile_height: width and height of the tile as int
"""
from __future__ import annotations

from pathlib import Path
import json
import pygame as pg


sprite_sheet_folder = Path(__file__).parent / "sprite-sheet"


class SheetSprite:
    """
    A sprite is a rectangular area of an image and can be constructed with:
    [x, y, width, height]
    or
    [x, y, width, height, scale]
    or
    [x, y, width, height, loop_x, loop_y]
    or
    [x, y, width, height, loop_x, loop_y, scale]
    """

    def __init__(
            self, image: pg.Surface, x: int, y: int, width: int, height: int, scale: float = 1, loop_x: int = 0,
            loop_y: int = 0
    ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.scale = scale
        self.loop_x = loop_x
        self.loop_y = loop_y
        self.sprite: pg.Surface | list[pg.Surface] = self.generate_image(image)

    def generate_image(self, image: pg.Surface) -> pg.Surface | list[pg.Surface]:
        """
        Generate an image from the sprite
        :param image:
        :return:
        """
        subsurface = image.subsurface(self.x, self.y, self.width, self.height)
        if self.loop_x == 0 and self.loop_y == 0:
            if self.scale == 1:
                return subsurface
            return pg.transform.scale(subsurface, (int(self.width * self.scale), int(self.height * self.scale)))

        sprites = []
        for i in range(subsurface.get_width() // self.loop_x):
            for j in range(subsurface.get_height() // self.loop_y):
                sprite = subsurface.subsurface(i * self.loop_x, j * self.loop_y, self.loop_x, self.loop_y)
                if self.scale == 1:
                    sprites.append(sprite)
                else:
                    sprites.append(
                        pg.transform.scale(sprite, (int(self.loop_x * self.scale), int(self.loop_y * self.scale)))
                    )
        return sprites


class SpriteSheet:
    """
    A sprite sheet is a collection of sprites and can be constructed with:
    [x, y, width, height]
    or
    [x, y, width, height, scale]
    or
    [x, y, width, height, loop_x, loop_y]
    or
    [x, y, width, height, loop_x, loop_y, scale]

    SpriteSheet is a dictionary with the following format:
    {
        "normal": [x, y, width, height],
        "scaled": [x, y, width, height, scale],
        "tiled": [x, y, width, height, tile_width, tile_height],
        "tiled_and_scaled": [x, y, width, height, tile_width, tile_height, scale]
    }
    """

    def __init__(self, image: pg.Surface, data: dict[str, list[int]]):
        self.image = image
        self.data = data
        self.sprites = {}

        for key, value in data.items():
            self.sprites[key] = self.get_sprite(value)

    def get_sprite(self, data: list[int]) -> SheetSprite:
        """
        Get a sprite from the sprite sheet
        """
        if len(data) == 4:
            return SheetSprite(self.image, data[0], data[1], data[2], data[3])
        elif len(data) == 5:
            return SheetSprite(self.image, data[0], data[1], data[2], data[3], data[4])
        elif len(data) == 6:
            return SheetSprite(self.image, data[0], data[1], data[2], data[3], loop_x=data[4],
                               loop_y=data[5])
        elif len(data) == 7:
            return SheetSprite(self.image, data[0], data[1], data[2], data[3], loop_x=data[4],
                               loop_y=data[5], scale=data[6])
        else:
            raise ValueError(f"Invalid sprite sheet data: {data}")


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
