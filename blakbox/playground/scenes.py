import blakbox
import blakbox.playground.elements as elements

class Launcher(blakbox.scene.BOXscene):
    def __init__(self, app) -> None:
        super().__init__(app, tile_size=[64, 64], grid_size=[100, 100])

    def init(self):
        self.interface.set_element("e1", elements.PlayButton(self.app, self.cache.get_font("megamax")))

    def exit(self):
        blakbox.log.BOXlogger.info("[BOXscene] Scene Exiting...")

    def events(self): pass
    def update(self, dt: float):
        self.cache.update_animation("logo-anim", dt)

    def render(self): pass

class Main(blakbox.scene.BOXscene):
    def __init__(self, app) -> None:
        super().__init__(app, tile_size=[64, 64], grid_size=[100, 100])
    
    def init(self):
        # self.renderer.set_flag(self.renderer.flags.DEBUG_CAMERA)
        self.renderer.set_flag(self.renderer.flags.DEBUG_OBJECT)
        self.renderer.set_flag(self.renderer.flags.DEBUG_TILEMAP)

        self.o1 = blakbox.resource.BOXobject(size=[32, 32], color=[255, 0, 0])
        self.interface.set_element("e1", elements.MenuButton(self.app, self.cache.get_font("megamax")))

    def exit(self):
        blakbox.log.BOXlogger.info("[BOXscene] Scene Exiting...")

    def events(self):
        if self.app.events.mouse_wheel_up:
            self.camera.mod_viewport(-2.5)
        if self.app.events.mouse_wheel_down:
            self.camera.mod_viewport(2.5)

        if self.app.events.mouse_pressed(blakbox.app.BOXmouse.RightClick):
            self.o1.move_to(blakbox.app.BOXmouse.pos.world)

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
        self.cache.update_animation("logo-anim", dt)
        self.app.window.mod_title(f"{self.app.clock.fps}")

    def render(self):
        self.renderer.commit(self.o1, self.cache.get_animation_frame("logo-anim"))