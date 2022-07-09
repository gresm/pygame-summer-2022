from __future__ import annotations

from warnings import warn

import pygame as pg


class SoundManager:
    def __init__(
            self, sounds: dict[str, pg.mixer.Sound], bgm_channel: int | pg.mixer.Channel | None = None,
            sfx_channel: int | pg.mixer.Channel | None = None
    ):
        if bgm_channel is None:
            bgm_channel = pg.mixer.find_channel(True)
        if sfx_channel is None:
            sfx_channel = pg.mixer.find_channel(False)

        self.bgm_channel = bgm_channel if isinstance(bgm_channel, pg.mixer.Channel) else pg.mixer.Channel(bgm_channel)
        self.sfx_channel = sfx_channel if isinstance(sfx_channel, pg.mixer.Channel) else pg.mixer.Channel(sfx_channel)
        self._global_volume = 1.0
        self.bgm_channel.set_volume(self.global_volume)
        self.sfx_channel.set_volume(self.global_volume)

        self._background_music_on = False
        self.sounds: dict[str, pg.mixer.Sound] = sounds
        self.background_music: pg.mixer.Sound | None = None

    @property
    def global_volume(self):
        return self._global_volume

    @global_volume.setter
    def global_volume(self, value: float):
        self._global_volume = value
        self.bgm_channel.set_volume(value)
        self.sfx_channel.set_volume(value)

    @property
    def play_background_music(self):
        return self._background_music_on

    @play_background_music.setter
    def play_background_music(self, value: bool):
        if value:
            self.play_bgm()
        else:
            self.stop_bgm()
        self._background_music_on = value

    def play_bgm(self, bgm: pg.mixer.Sound | None = None):
        if bgm is None:
            bgm = self.background_music

        if bgm is None:
            return

        self.background_music = bgm
        self.bgm_channel.play(bgm, -1)
        self._background_music_on = True

    def stop_bgm(self):
        self.background_music.stop()
        self._background_music_on = False

    def play_sfx(self, sfx: pg.mixer.Sound | str):
        if isinstance(sfx, str):
            if sfx not in self.sounds:
                warn(f"Sound \"{sfx}\" not found in sounds dict.")
            sfx = self.sounds[sfx]
        self.sfx_channel.play(sfx)
