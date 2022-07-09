from __future__ import annotations

import pygame as pg


class SoundManager:
    def __init__(
            self, bgm_channel: int | pg.mixer.Channel | None = None, sfx_channel: int | pg.mixer.Channel | None = None
    ):
        if bgm_channel is None:
            bgm_channel = pg.mixer.find_channel(True)
        if sfx_channel is None:
            sfx_channel = pg.mixer.find_channel(False)

        self.bgm_channel = bgm_channel if isinstance(bgm_channel, pg.mixer.Channel) else pg.mixer.Channel(bgm_channel)
        self.sfx_channel = sfx_channel if isinstance(sfx_channel, pg.mixer.Channel) else pg.mixer.Channel(sfx_channel)
        self.global_volume = 1.0
        self.bgm_channel.set_volume(self.global_volume)
        self.sfx_channel.set_volume(self.global_volume)

        self._background_music_on = False
        self.sounds: dict[str, pg.mixer.Sound] = {}
        self.background_music: pg.mixer.Sound | None = None

    @property
    def background_music_on(self):
        return self._background_music_on

    @background_music_on.setter
    def background_music_on(self, value: bool):
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
        self.background_music.set_volume(self.global_volume)
        self.bgm_channel.play(bgm, -1)
        self._background_music_on = True

    def stop_bgm(self):
        self.background_music.stop()
        self._background_music_on = False
