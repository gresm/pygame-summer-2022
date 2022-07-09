import pygame as pg
import json

from pathlib import Path

images_folder = Path(__file__).parent / "images"
images_config_file = images_folder / "images.json"
with open(images_config_file, "r") as f:
    images_config = json.load(f)

images = {name: pg.image.load(str(images_folder / file)) for name, file in images_config.items()}
