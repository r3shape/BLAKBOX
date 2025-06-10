import pygame as pg
import blakbox

class PlayButton(blakbox.resource.BOXlabel):
    def __init__(self, app: blakbox.app.BOXapp, font: pg.Font) -> None:
        super().__init__(font=font, text="Play", size=[164, 64], text_pos=[56, 40], flags=blakbox.resource.BOXelement.flags.SHOW_TEXT)
        self.app: blakbox.app.BOXapp = app
        self.pos = [self.app.window.screen_size[0] / 2 - self.size[0] / 2,
                    self.app.window.screen_size[1] / 2 - self.size[1] / 2, ]
        self.border_width = 2
        self.color = [200, 200, 200]
        self.border_color = [0, 0, 0]

    def on_click(self) -> None:
        self.app.set_scene("Main")

    def on_hover(self) -> None:
        self.color = [180, 180, 180]
        self.border_color = [20, 20, 20]

    def on_unhover(self) -> None:
        self.color = [200, 200, 200]
        self.border_color = [0, 0, 0]

    def on_render(self, surface):
        surface.blit(self.app.cache.get_animation_frame("logo-anim"), [64, 8])

class MenuButton(blakbox.resource.BOXlabel):
    def __init__(self, app: blakbox.app.BOXapp, font: pg.Font) -> None:
        super().__init__(font=font, text="Menu", text_pos=[0, 0], flags=blakbox.resource.BOXelement.flags.SHOW_TEXT)
        self.app: blakbox.app.BOXapp = app
       
        self.border_width = 2
        self.color = [200, 200, 200]
        self.border_color = [0, 0, 0]

    def on_click(self) -> None:
        self.app.set_scene("Launcher")

    def on_hover(self) -> None:
        self.color = [180, 180, 180]
        self.border_color = [20, 20, 20]

    def on_unhover(self) -> None:
        self.color = [200, 200, 200]
        self.border_color = [0, 0, 0]
