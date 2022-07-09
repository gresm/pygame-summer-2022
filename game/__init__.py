import pygame as pg

from gamelib import get_game, scene_manager, SoundManager
from . import constants
from .scenes import MainMenu


pg.init()

game = get_game((constants.WIDTH, constants.HEIGHT), constants.MAX_FPS)

mixer = SoundManager()
scene_manager.init(game, mixer)
scene_manager.spawn_scene(MainMenu)


@game.frame
def frame(window: pg.Surface, delta_time: float):
    for ev in pg.event.get():
        if ev.type == pg.QUIT:
            game.stop()
        else:
            scene_manager.handle_events(ev)

    scene_manager.update(delta_time)

    window.fill((0, 0, 0))

    scene_manager.draw(window)

    pg.display.update()


def main():
    game.init()
    game.run()
