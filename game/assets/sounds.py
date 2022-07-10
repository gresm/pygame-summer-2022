# sound.py
import pygame as pg
import json

from pathlib import Path

sounds_folder = Path(__file__).parent / "sounds"
sounds_config_file = sounds_folder / "sounds.json"

with open(sounds_config_file, "r") as f:
    images_config = json.load(f)

sounds = {name: pg.mixer.Sound(str(sounds_folder / file)) for name, file in images_config.items()}


__all__ = ["sounds"]
