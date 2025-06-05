import blakbox
import blakbox.playground.elements as elements

class Launcher(blakbox.scene.BOXscene):
    def __init__(self, app) -> None:
        super().__init__(app, tile_size=[64, 64], grid_size=[100, 100])

    def init(self):
        self.interface.set_flag(self.interface.flags.DISPLAY_LIST)
        self.interface.set_element("play", elements.PlayButton(self, self.cache.get_font("f1")))

    def exit(self): pass
    def events(self): pass
    def update(self, dt: float): pass
    def render(self): pass

class Main(blakbox.scene.BOXscene):
    def __init__(self, app) -> None:
        super().__init__(app, tile_size=[64, 64], grid_size=[100, 100])
    
    def init(self):
        self.renderer.set_flag(self.renderer.flags.DEBUG_CAMERA)
        self.renderer.set_flag(self.renderer.flags.DEBUG_OBJECT)
        self.renderer.set_flag(self.renderer.flags.DEBUG_TILEMAP)

        self.o1 = blakbox.resource.BOXobject(size=[32, 32], color=[255, 0, 0])
        self.cache.load_surface("s1", blakbox.utils.rel_path("assets/images/geo.png"))

    def exit(self):
        blakbox.log.BOXlogger.info("Scene Exiting...")

    def events(self):
        if self.app.events.mouse_wheel_up:
            self.camera.mod_viewport(-2.5)
        if self.app.events.mouse_wheel_down:
            self.camera.mod_viewport(2.5)

        if self.app.events.key_held(blakbox.app.BOXkeyboard.W):
            self.o1.move(up=1)
        else: self.o1.move(up=0)

        if self.app.events.key_held(blakbox.app.BOXkeyboard.S):
            self.o1.move(down=1)
        else: self.o1.move(down=0)

        if self.app.events.key_held(blakbox.app.BOXkeyboard.A):
            self.o1.move(left=1)
        else: self.o1.move(left=0)

        if self.app.events.key_held(blakbox.app.BOXkeyboard.D):
            self.o1.move(right=1)
        else: self.o1.move(right=0)

    def update(self, dt: float):
        self.o1.update(dt)
        self.camera.follow(self.o1)
        self.app.window.mod_title(f"{self.app.clock.fps}")

    def render(self):
        self.renderer.commit(self.o1, self.cache.get_surface("s1"))