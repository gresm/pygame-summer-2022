from gamelib import BaseScene


class QuitScene(BaseScene):
    def after_init(self):
        self.manager.game.stop()


__all__ = ["QuitScene"]
