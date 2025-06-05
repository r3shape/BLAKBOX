import blakbox
import blakbox.playground.scenes as scenes

class Playground(blakbox.app.BOXapp):
    def __init__(self) -> None:
        super().__init__("Blakbox Playground", [255, 255, 255], [1280, 720], [1280*2, 720*2])

    def init(self) -> None:
        blakbox.log.BOXlogger.debug("Welcome to the Blakbox Playground!")
        blakbox.log.BOXlogger.debug("Hosted by your's truly @r3shape <3")

        self.cache.load_surface("s1", blakbox.utils.rel_path("assets/images/geo.png"))
        self.cache.load_font("f1", blakbox.utils.box_path("assets/fonts/slkscr.ttf"), 18)

        self.add_scene("Launcher", scenes.Launcher)
        self.add_scene("Main", scenes.Main)
        self.set_scene("Launcher")

    def exit(self) -> None: pass

def main() -> None:
    Playground().run()
