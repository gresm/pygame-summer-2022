from __future__ import annotations

from warnings import warn

import pygame as pg


ChannelClass = type(pg.mixer.Channel(0))


class SoundManager:
    def __init__(
            self, sounds: dict[str, pg.mixer.Sound] | None = None, bgm_channel: int | pg.mixer.Channel | None = None,
            sfx_channel: int | pg.mixer.Channel | None = None
    ):
        if bgm_channel is None:
            bgm_channel = pg.mixer.find_channel(True)
        if sfx_channel is None:
            sfx_channel = pg.mixer.find_channel(False)

        self.bgm_channel = bgm_channel if isinstance(bgm_channel, ChannelClass) else pg.mixer.Channel(bgm_channel)
        self.sfx_channel = sfx_channel if isinstance(sfx_channel, ChannelClass) else pg.mixer.Channel(sfx_channel)
        self._global_volume = 1.0
        self.bgm_channel.set_volume(self.global_volume)
        self.sfx_channel.set_volume(self.global_volume)

        self._background_music_on = False
        self.sounds: dict[str, pg.mixer.Sound] = sounds if sounds is not None else {}
        self.background_music: pg.mixer.Sound | None = None
        self._bgm_enabled: bool = True

    @property
    def global_volume(self):
        return self._global_volume

    @global_volume.setter
    def global_volume(self, value: float):
        self._global_volume = value
        self.bgm_channel.set_volume(value)
        self.sfx_channel.set_volume(value)

    @property
    def bgm_enabled(self) -> bool:
        return self._bgm_enabled

    @bgm_enabled.setter
    def bgm_enabled(self, value: bool):
        self._bgm_enabled = value
        if value:
            self.play_bgm()
        else:
            self.stop_bgm()

    @property
    def bgm_playing(self) -> bool:
        return self._background_music_on

    def play_bgm(self, bgm: pg.mixer.Sound | str | None = None):
        if self.bgm_playing:
            if bgm is self.background_music or bgm is None:
                return
            elif bgm in self.sounds and self.sounds[bgm] is self.background_music:
                return

        if bgm is None:
            bgm = self.background_music

        if bgm is None:
            warn("No background music set.")
            return

        if isinstance(bgm, str):
            if bgm not in self.sounds:
                warn(f"Sound \"{bgm}\" not found in sounds dict.")
                return
            bgm = self.sounds[bgm]

        self.background_music = bgm

        if not self.bgm_enabled:
            return

        self.bgm_channel.play(bgm, -1)
        self._background_music_on = True

    def stop_bgm(self):
        print("stopping")
        self.bgm_channel.stop()
        self._background_music_on = False

    def play_sfx(self, sfx: pg.mixer.Sound | str):
        if isinstance(sfx, str):
            if sfx not in self.sounds:
                warn(f"Sound \"{sfx}\" not found in sounds dict.")
            sfx = self.sounds[sfx]
        self.sfx_channel.play(sfx)

    def add_sfx(self, name: str, sound: pg.mixer.Sound):
        self.sounds[name] = sound


__all__ = ["SoundManager"]
