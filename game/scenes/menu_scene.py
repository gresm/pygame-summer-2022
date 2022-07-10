from __future__ import annotations

import webbrowser
import pygame as pg

from .quit_scene import QuitScene
from .template_gui_scene import TemplateGUIScene, SecondTemplate
from .gui_scene import draw_line_under_rect
from .credits_scene import CreditsMenu


class MainMenu(TemplateGUIScene):
    def after_init(self):
        super().after_init()

        self.create_button("title", "Main Menu", "title", is_title=True)
        self.create_button("new-game", "New Game", "button-1")
        self.create_button("setting", "Setting", "button-2")
        self.create_button("quit", "Quit", "button-3")

    def option_selected(self, option: str):
        if option == "new-game":
            pass
        elif option == "setting":
            self.manager.spawn_remove_scene(SettingsMenu)
        elif option == "quit":
            self.manager.spawn_remove_scene(QuitScene)
        elif option == "title":
            webbrowser.open("https://rrrlead.itch.io/the-climb")


class SettingsMenu(TemplateGUIScene):
    def after_init(self):
        super().after_init()

        self.create_button("title", "Settings", "title", is_title=True)
        self.create_button("back", "<- Back", "top-left")
        self.create_button("music", "Music", "button-1")
        self.create_button("credits", "Credits", "button-2")
        self.create_button("display", "Display", "button-3")

    def option_selected(self, option: str):
        if option == "back":
            self.manager.spawn_remove_scene(MainMenu)
        elif option == "music":
            self.manager.spawn_remove_scene(MusicMenu)
        elif option == "credits":
            self.manager.spawn_remove_scene(CreditsMenu)
        elif option == "display":
            self.manager.spawn_remove_scene(DisplayMenu)
        elif option == "title":
            webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ")


class MusicMenu(SecondTemplate):
    def after_init(self):
        super().after_init()
        self.create_locations()
        self.create_button("title", "Music", "title", is_title=True)
        self.setup_widget()

        self.create_button("back", "<- Back", "back")
        self.create_button("bgm-enabled", "BGM: enabled", "button-1")
        self.create_button("volume", "          ", "button-2")
        self.create_button("button-3", "Button 3", "button-3")

        self.create_location("volume-title", (0, -30), "center", "center", "volume")
        self.create_button("volume-title", "Volume:", "volume-title")

        self.create_button("bgm-disabled", "BGM: disabled", "button-1")
        self.disable_button("bgm-disabled")


class DisplayMenu(TemplateGUIScene):
    full_screen: bool
    borderless: bool
    scaled: bool

    def init(self):
        super().init()
        self.full_screen = False
        self.borderless = False
        self.scaled = False

    def after_init(self):
        super().after_init()

        self.create_button("title", "Display", "title", is_title=True)
        self.create_button("back", "<- Back", "top-left")
        self.create_button("apply", "Apply", "top-right")

        self.create_button("full-screen", "Full screen", "button-1")
        self.create_button("no-border", "Borderless", "button-2")
        self.create_button("scaled", "Scaled", "button-3")

        self.create_button("windowed", "Windowed", "button-1")
        self.disable_button("bordered")

        self.create_button("border", "With borders", "button-2")
        self.disable_button("border")

        self.create_button("no-scale", "Not scaled", "button-3")
        self.disable_button("no-scale")

    def option_selected(self, option: str):
        if option == "back":
            self.manager.spawn_remove_scene(SettingsMenu)
        elif option == "apply":
            self.apply_settings()
        elif option == "full-screen":
            self.full_screen = not self.full_screen
            self.toggle_button("full-screen")
            self.toggle_button("windowed")
        elif option == "no-border":
            self.borderless = not self.borderless
            self.toggle_button("no-border")
            self.toggle_button("border")
        elif option == "scaled":
            self.scaled = not self.scaled
            self.toggle_button("scaled")
            self.toggle_button("no-scale")
        elif option == "windowed":
            self.full_screen = not self.full_screen
            self.toggle_button("windowed")
            self.toggle_button("full-screen")
        elif option == "border":
            self.borderless = not self.borderless
            self.toggle_button("border")
            self.toggle_button("no-border")
        elif option == "no-scale":
            self.scaled = not self.scaled
            self.toggle_button("no-scale")
            self.toggle_button("scaled")
        elif option == "title":
            print("Imagine that an error occurred with setting up the window.")
            pg.base.segfault()

    def apply_settings(self):
        flag = 0
        if self.full_screen:
            flag |= pg.FULLSCREEN
        if self.borderless:
            flag |= pg.NOFRAME
        if self.scaled:
            flag |= pg.SCALED

        self.manager.game.set_flags(flag)


__all__ = ["MainMenu", "TemplateGUIScene"]
