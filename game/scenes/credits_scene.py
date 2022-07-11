import pygame as pg
from .template_gui_scene import SecondTemplate


class CreditsMenu(SecondTemplate):
    def after_init(self):
        super().after_init()
        self.create_locations()
        self.create_button("title", "Credits", "title", is_title=True)
        self.setup_widget()
