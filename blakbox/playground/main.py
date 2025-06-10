import blakbox
import scenes as scenes

class Playground(blakbox.app.BOXapp):
    def __init__(self) -> None:
        super().__init__("Blakbox Playground", [255, 255, 255], [1280, 720], [1280*2, 720*2])

    def init(self) -> None:
        blakbox.log.BOXlogger.debug("Welcome to the Blakbox Playground!")
        blakbox.log.BOXlogger.debug("Hosted by your's truly @r3shape <3")

        self.cache.load_font("slkscr", blakbox.utils.box_path("assets/fonts/slkscr.ttf"), 18)
        self.cache.load_font("megamax", blakbox.utils.box_path("assets/fonts/megamax.ttf"), 18)
        self.cache.load_surface("logo", blakbox.utils.box_path("assets/images/logo-anim.png"))
        self.cache.load_animation("logo-anim", blakbox.utils.box_path("assets/images/logo-anim.png"), [32, 32], 12)

        self.add_scene("Launcher", scenes.Launcher)
        self.add_scene("Main", scenes.Main)
        self.set_scene("Launcher")

    def exit(self) -> None: pass

Playground().run()
