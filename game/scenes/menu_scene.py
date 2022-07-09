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
                    self.manager.spawn_scene(SettingsMenu)
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


class SettingsMenu(BaseScene):
    menu_text: pg.Surface
    menu_text_rect: pg.Rect
    screen_rect: pg.Rect
    widgets_rect: pg.Rect

    music_rect: pg.Rect
    music_text: pg.Surface

    resolution_rect: pg.Rect
    resolution_text: pg.Surface

    back_rect: pg.Rect
    back_text: pg.Surface

    credits_rect: pg.Rect
    credits_text: pg.Surface

    currently_selecting: int

    def init(self):
        pg.display.set_caption("The Climb - Settings", "The climb")
        self.menu_text = assets.title_font.render("Settings", True, (255, 255, 255))
        self.music_text = assets.text_font.render("Sound", True, (255, 255, 255))
        self.resolution_text = assets.text_font.render("Resolution", True, (255, 255, 255))
        self.credits_text = assets.text_font.render("Credits", True, (255, 255, 255))
        self.back_text = assets.text_font.render("<- Back", True, (255, 255, 255))

        self.menu_text_rect = self.menu_text.get_rect()
        self.music_rect = self.music_text.get_rect()
        self.credits_rect = self.credits_text.get_rect()
        self.resolution_rect = self.resolution_text.get_rect()
        self.back_rect = self.back_text.get_rect()
        self.back_rect.x = 10

        self.currently_selecting = 0

    def after_init(self):
        self.screen_rect = self.manager.game.screen.get_rect()
        self.widgets_rect = pg.Rect(0, 0, self.screen_rect.width - 400, 100)
        self.menu_text_rect.midtop = pg.Vector2(self.screen_rect.midtop) + pg.Vector2(0, 20)
        self.widgets_rect.midbottom = pg.Vector2(self.screen_rect.midbottom) - pg.Vector2(0, 50)

        self.credits_rect.center = self.widgets_rect.center
        self.music_rect.midleft = pg.Vector2(self.widgets_rect.midleft) + pg.Vector2(50, 0)
        self.resolution_rect.midright = pg.Vector2(self.widgets_rect.midright) - pg.Vector2(50, 0)

    def draw(self, window: pg.Surface):
        pg.draw.rect(window, (0, 0, 0), self.widgets_rect)
        pg.draw.rect(window, (255, 255, 255), self.widgets_rect, 5)

        window.blit(self.menu_text, self.menu_text_rect)
        window.blit(self.music_text, self.music_rect)
        window.blit(self.credits_text, self.credits_rect)
        window.blit(self.resolution_text, self.resolution_rect)
        window.blit(self.back_text, self.back_rect)

        if self.currently_selecting == 1:
            draw_line_under_rect(window, (255, 255, 255), self.music_rect)
        elif self.currently_selecting == 2:
            draw_line_under_rect(window, (255, 255, 255), self.credits_rect)
        elif self.currently_selecting == 3:
            draw_line_under_rect(window, (255, 255, 255), self.resolution_rect)
        elif self.currently_selecting == 4:
            draw_line_under_rect(window, (255, 255, 255), self.menu_text_rect)
        elif self.currently_selecting == 5:
            draw_line_under_rect(window, (255, 255, 255), self.back_rect)

    def update(self, delta_time: float):
        for event in self.get_events():
            if event.type == pg.MOUSEBUTTONDOWN:
                if self.currently_selecting == 1:
                    self.manager.spawn_scene(MusicMenu)
                elif self.currently_selecting == 2:
                    pass
                elif self.currently_selecting == 3:
                    self.manager.spawn_scene(ResolutionMenu)
                elif self.currently_selecting == 4:
                    webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
                elif self.currently_selecting == 5:
                    self.manager.spawn_scene(MainMenu)

        mouse_pos = pg.mouse.get_pos()

        if self.music_rect.collidepoint(mouse_pos):
            self.currently_selecting = 1
        elif self.credits_rect.collidepoint(mouse_pos):
            self.currently_selecting = 2
        elif self.resolution_rect.collidepoint(mouse_pos):
            self.currently_selecting = 3
        elif self.menu_text_rect.collidepoint(mouse_pos):
            self.currently_selecting = 4
        elif self.back_rect.collidepoint(mouse_pos):
            self.currently_selecting = 5
        else:
            self.currently_selecting = 0


class ResolutionMenu(BaseScene):
    menu_text: pg.Surface
    menu_text_rect: pg.Rect
    screen_rect: pg.Rect
    widgets_rect: pg.Rect

    full_screen_text: pg.Surface
    full_screen_toggled_text: pg.Surface
    full_screen_rect: pg.Rect
    is_full_screen: bool

    no_frame_text: pg.Surface
    no_frame_toggled_text: pg.Surface
    no_frame_rect: pg.Rect
    is_no_frame: bool

    scaled_text: pg.Surface
    scaled_toggled_text: pg.Surface
    scaled_rect: pg.Rect
    is_scaled: bool

    back_rect: pg.Rect
    back_text: pg.Surface

    apply_rect: pg.Rect
    apply_text: pg.Surface

    currently_selecting: int

    def init(self):
        pg.display.set_caption("The Climb - Resolution", "The climb")

        self.is_full_screen = False
        self.is_no_frame = False
        self.is_scaled = False

        self.menu_text = assets.title_font.render("Resolution", True, (255, 255, 255))
        self.menu_text_rect = self.menu_text.get_rect()

        self.full_screen_text = assets.text_font.render("Full Screen", True, (255, 255, 255))
        self.full_screen_toggled_text = assets.text_font.render("Windowed", True, (255, 255, 255))
        self.full_screen_rect = self.full_screen_text.get_rect()

        self.no_frame_text = assets.text_font.render("No Frame", True, (255, 255, 255))
        self.no_frame_toggled_text = assets.text_font.render("Frame", True, (255, 255, 255))
        self.no_frame_rect = self.no_frame_text.get_rect()

        self.scaled_text = assets.text_font.render("Scaled", True, (255, 255, 255))
        self.scaled_toggled_text = assets.text_font.render("Unscaled", True, (255, 255, 255))
        self.scaled_rect = self.scaled_text.get_rect()

        self.back_text = assets.text_font.render("<- Back", True, (255, 255, 255))
        self.back_rect = self.back_text.get_rect()
        self.back_rect.x = 10

        self.apply_text = assets.text_font.render("Apply", True, (255, 255, 255))
        self.apply_rect = self.apply_text.get_rect()

        self.currently_selecting = 0

    def after_init(self):
        self.screen_rect = self.manager.game.screen.get_rect()
        self.widgets_rect = pg.Rect(0, 0, self.screen_rect.width - 400, 100)
        self.menu_text_rect.midtop = pg.Vector2(self.screen_rect.midtop) + pg.Vector2(0, 20)
        self.widgets_rect.midbottom = pg.Vector2(self.screen_rect.midbottom) - pg.Vector2(0, 50)

        self.full_screen_rect.midleft = pg.Vector2(self.widgets_rect.midleft) + pg.Vector2(50, 0)
        self.no_frame_rect.center = self.widgets_rect.center
        self.scaled_rect.midright = pg.Vector2(self.widgets_rect.midright) - pg.Vector2(50, 0)
        self.apply_rect.right = self.screen_rect.right - 10

    def draw(self, window: pg.Surface):
        pg.draw.rect(window, (0, 0, 0), self.widgets_rect)
        pg.draw.rect(window, (255, 255, 255), self.widgets_rect, 5)

        window.blit(self.menu_text, self.menu_text_rect)
        window.blit(self.back_text, self.back_rect)
        window.blit(self.full_screen_text, self.full_screen_rect)
        window.blit(self.no_frame_text, self.no_frame_rect)
        window.blit(self.scaled_text, self.scaled_rect)
        window.blit(self.apply_text, self.apply_rect)

        if self.currently_selecting == 1:
            draw_line_under_rect(window, (255, 255, 255), self.full_screen_rect)
        elif self.currently_selecting == 2:
            draw_line_under_rect(window, (255, 255, 255), self.no_frame_rect)
        elif self.currently_selecting == 3:
            draw_line_under_rect(window, (255, 255, 255), self.scaled_rect)
        elif self.currently_selecting == 4:
            draw_line_under_rect(window, (255, 255, 255), self.menu_text_rect)
        elif self.currently_selecting == 5:
            draw_line_under_rect(window, (255, 255, 255), self.back_rect)
        elif self.currently_selecting == 6:
            draw_line_under_rect(window, (255, 255, 255), self.apply_rect)

    def apply_changes(self):
        flag = 0
        if self.is_full_screen:
            flag |= pg.FULLSCREEN
        if self.is_no_frame:
            flag |= pg.NOFRAME
        if self.is_scaled:
            flag |= pg.SCALED

        self.manager.game.set_flags(flag)

    def update(self, delta_time: float):
        for event in self.get_events():
            if event.type == pg.MOUSEBUTTONDOWN:
                if self.currently_selecting == 1:
                    self.full_screen_text, self.full_screen_toggled_text = self.full_screen_toggled_text, \
                                                                           self.full_screen_text
                    self.is_full_screen = not self.is_full_screen
                elif self.currently_selecting == 2:
                    self.no_frame_text, self.no_frame_toggled_text = self.no_frame_toggled_text, self.no_frame_text
                    self.is_no_frame = not self.is_no_frame
                elif self.currently_selecting == 3:
                    self.scaled_text, self.scaled_toggled_text = self.scaled_toggled_text, self.scaled_text
                    self.is_scaled = not self.is_scaled
                elif self.currently_selecting == 4:
                    pass
                elif self.currently_selecting == 5:
                    self.manager.spawn_scene(SettingsMenu)
                elif self.currently_selecting == 6:
                    self.apply_changes()

        mouse_pos = pg.mouse.get_pos()

        if self.full_screen_rect.collidepoint(mouse_pos):
            self.currently_selecting = 1
        elif self.no_frame_rect.collidepoint(mouse_pos):
            self.currently_selecting = 2
        elif self.scaled_rect.collidepoint(mouse_pos):
            self.currently_selecting = 3
        elif self.menu_text_rect.collidepoint(mouse_pos):
            self.currently_selecting = 4
        elif self.back_rect.collidepoint(mouse_pos):
            self.currently_selecting = 5
        elif self.apply_rect.collidepoint(mouse_pos):
            self.currently_selecting = 6
        else:
            self.currently_selecting = 0


class MusicMenu(BaseScene):
    menu_text: pg.Surface
    menu_text_rect: pg.Rect
    screen_rect: pg.Rect
    widgets_rect: pg.Rect

    music_rect: pg.Rect
    music_text: pg.Surface

    back_rect: pg.Rect
    back_text: pg.Surface

    currently_selecting: int

    def init(self):
        pg.display.set_caption("The Climb - Music", "The climb")
        self.menu_text = assets.title_font.render("Music", True, (255, 255, 255))
        self.music_text = assets.text_font.render("Music", True, (255, 255, 255))
        self.back_text = assets.text_font.render("<- Back", True, (255, 255, 255))

        self.menu_text_rect = self.menu_text.get_rect()
        self.music_rect = self.music_text.get_rect()
        self.back_rect = self.back_text.get_rect()

        self.currently_selecting = 0

    def after_init(self):
        self.screen_rect = self.manager.game.screen.get_rect()
        self.widgets_rect = pg.Rect(0, 0, self.screen_rect.width - 400, 100)
        self.menu_text_rect.midtop = pg.Vector2(self.screen_rect.midtop) + pg.Vector2(0, 20)
        self.widgets_rect.midbottom = pg.Vector2(self.screen_rect.midbottom) - pg.Vector2(0, 50)

        self.music_rect.center = self.widgets_rect.center

    def draw(self, window: pg.Surface):
        pg.draw.rect(window, (0, 0, 0), self.widgets_rect)
        pg.draw.rect(window, (255, 255, 255), self.widgets_rect, 5)

        window.blit(self.menu_text, self.menu_text_rect)


__all__ = ['MainMenu']
