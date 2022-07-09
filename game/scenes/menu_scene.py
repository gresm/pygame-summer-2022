from __future__ import annotations

import webbrowser

from .quit_scene import QuitScene
from .template_gui_scene import TemplateGUIScene
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
        self.create_button("res", "Resolution", "button-3")

    def option_selected(self, option: str):
        if option == "back":
            self.manager.spawn_remove_scene(MainMenu)
        elif option == "music":
            self.manager.spawn_remove_scene(MusicMenu)
        elif option == "credits":
            self.manager.spawn_remove_scene(CreditsMenu)
        elif option == "res":
            self.manager.spawn_remove_scene(ResolutionMenu)


class MusicMenu(TemplateGUIScene):
    pass


class ResolutionMenu(TemplateGUIScene):
    pass


__all__ = ["MainMenu", "TemplateGUIScene"]
