import webbrowser
import pygame as pg
from gamelib import BaseScene

from .. import assets

from .quit_scene import QuitScene


def draw_line_under_rect(surface: pg.Surface, color: tuple[int, int, int], rect: pg.Rect):
    pg.draw.line(surface, color, rect.bottomleft, rect.bottomright)


class MainMenu(BaseScene):
    menu_text: pg.Surface
    menu_text_rect: pg.Rect
    screen_rect: pg.Rect
    widgets_rect: pg.Rect

    play_rect: pg.Rect
    play_text: pg.Surface

    settings_rect: pg.Rect
    settings_text: pg.Surface

    quit_rect: pg.Rect
    quit_text: pg.Surface

    currently_selecting: int

    def init(self):
        pg.display.set_caption("The Climb - Main menu", "The climb")
        self.menu_text = assets.title_font.render("Main Menu", True, (255, 255, 255))
        self.play_text = assets.text_font.render("Play", True, (255, 255, 255))
        self.settings_text = assets.text_font.render("Settings", True, (255, 255, 255))
        self.quit_text = assets.text_font.render("Quit", True, (255, 255, 255))

        self.menu_text_rect = self.menu_text.get_rect()
        self.play_rect = self.play_text.get_rect()
        self.settings_rect = self.settings_text.get_rect()
        self.quit_rect = self.quit_text.get_rect()

        self.currently_selecting = 0

    def after_init(self):
        self.screen_rect = self.manager.game.screen.get_rect()
        self.widgets_rect = pg.Rect(0, 0, self.screen_rect.width - 400, 100)
        self.menu_text_rect.midtop = pg.Vector2(self.screen_rect.midtop) + pg.Vector2(0, 20)
        self.widgets_rect.midbottom = pg.Vector2(self.screen_rect.midbottom) - pg.Vector2(0, 50)

        self.play_rect.midleft = pg.Vector2(self.widgets_rect.midleft) + pg.Vector2(50, 0)
        self.settings_rect.center = self.widgets_rect.center
        self.quit_rect.midright = pg.Vector2(self.widgets_rect.midright) - pg.Vector2(50, 0)

    def draw(self, window: pg.Surface):
        pg.draw.rect(window, (0, 0, 0), self.widgets_rect)
        pg.draw.rect(window, (255, 255, 255), self.widgets_rect, 5)

        window.blit(self.menu_text, self.menu_text_rect)
        window.blit(self.play_text, self.play_rect)
        window.blit(self.settings_text, self.settings_rect)
        window.blit(self.quit_text, self.quit_rect)

        if self.currently_selecting == 1:
            draw_line_under_rect(window, (255, 255, 255), self.play_rect)
        elif self.currently_selecting == 2:
            draw_line_under_rect(window, (255, 255, 255), self.settings_rect)
        elif self.currently_selecting == 3:
            draw_line_under_rect(window, (255, 255, 255), self.quit_rect)
        elif self.currently_selecting == 4:
            draw_line_under_rect(window, (255, 255, 255), self.menu_text_rect)

    def update(self, delta_time: float):
        for event in self.get_events():
            if event.type == pg.MOUSEBUTTONDOWN:
                if self.currently_selecting == 1:
                    pass
                elif self.currently_selecting == 2:
                    pass
                elif self.currently_selecting == 3:
                    self.manager.spawn_scene(QuitScene)
                elif self.currently_selecting == 4:
                    webbrowser.open("https://pygame.org/")
        mouse_pos = pg.mouse.get_pos()
        if self.play_rect.collidepoint(mouse_pos):
            self.currently_selecting = 1
        elif self.settings_rect.collidepoint(mouse_pos):
            self.currently_selecting = 2
        elif self.quit_rect.collidepoint(mouse_pos):
            self.currently_selecting = 3
        elif self.menu_text_rect.collidepoint(mouse_pos):
            self.currently_selecting = 4
        else:
            self.currently_selecting = 0


__all__ = ['MainMenu']
