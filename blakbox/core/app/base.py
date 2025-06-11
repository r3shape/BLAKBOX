from ...utils import add_v2, mul_v2, div2_v2, div2_v2i
from ...globals import pg
from ...atom import BOXprivate, BOXatom
from ...log import BOXlogger
from .clock import BOXclock
from .window import BOXwindow
from .events import BOXevents
from .inputs import BOXmouse
from ..resource import BOXcache

from ..scene import BOXscene
from ..scene import BOXtilemap

class BOXapp(BOXatom):
    class flags:
        RUNNING: int = 1 << 0
        PAUSED: int = 1 << 1

    def __init__(
            self,
            title: str,
            clear_color: list[int],
            screen_size: list[int],
            display_size: list[int],
    ):
        super().__init__()
        self.title: str = title
        self.clock: BOXclock = BOXclock()
        self.cache: BOXcache = BOXcache(self)
        self.events: BOXevents = BOXevents(self)
        self.window: BOXwindow = BOXwindow(title, [1, 1], screen_size, display_size, clear_color)

        self.scene: BOXscene = None
        self.scenes: dict[str, BOXscene] = {}

        self.init()
        self.set_flag(self.flags.RUNNING)

    def init(self) -> None:
        BOXlogger.error(f'"{self.title}" Initialization Method Missing...')
        raise NotImplementedError
    
    def exit(self) -> None:
        BOXlogger.error(f'"{self.title}" Exit Method Missing...')
        raise NotImplementedError

    def add_scene(self, key: str, scene: BOXscene) -> None:
        if not isinstance(scene, type):
            BOXlogger.warning(f"[BOXapp] pass the scene as a type: (key){key}")
            return
        if self.scenes.get(key, False) != False:
            BOXlogger.warning(f"[BOXapp] scene already added: (key){key}")
            return
        self.scenes[key] = scene(self)
        BOXlogger.info(f"[BOXapp] scene added: (key){key}")

    def get_scene(self, key: str) -> BOXscene:
        if not isinstance(key, str): return
        if key not in self.scenes:
            BOXlogger.warning(f"[BOXapp] scene not found: (key){key}")
            return
        return self.scenes[key]

    def set_scene(self, key: str) -> None:
        if self.scenes.get(key, False) == False:
            BOXlogger.warning(f"[BOXapp] scene not found: (key){key}")
            return
        self.scene = self.scenes[key]
        BOXlogger.info(f"[BOXapp] scene set: (key){key}")
        self.scene.init()
        
    def rem_scene(self, key: str) -> None:
        if self.scenes.get(key, False) != False:
            BOXlogger.warning(f"[BOXapp] scene not found: (key){key}")
            return
        self.scenes.pop(key).exit()
        self.scene = None
        BOXlogger.info(f"[BOXapp] scene removed: (key){key}")

    def run(self) -> None:
        while self.get_flag(self.flags.RUNNING):
            self.clock.tick()
            self.events.update()
            if isinstance(self.scene, BOXscene):
                self.scene.events()
                self.scene.physics.update(self.clock.dt)
                self.scene.update(self.clock.dt)

                self.scene.camera.update(self.clock.dt)
                
                BOXmouse.pos.view = add_v2(div2_v2(BOXmouse.pos.screen, self.scene.camera.viewport_scale), self.scene.camera.pos)
                BOXmouse.pos.world = mul_v2(div2_v2i(BOXmouse.pos.view, self.scene.tilemap.tile_size), self.scene.tilemap.tile_size)
                
                self.scene.interface.update(self.events)
                if isinstance(self.scene.tilemap, BOXtilemap):
                    self.scene.tilemap.grid.update()
                self.scene.render()
                self.scene.renderer.flush()
                self.scene.interface.render()
            
            BOXmouse.pos.rel = pg.mouse.get_rel()
            BOXmouse.pos.screen = pg.mouse.get_pos()

            self.window.update()
            self.clock.update()
        else:
            if isinstance(self.scene, BOXscene):
                self.scene.interface.clear()
                self.scene.exit()
            self.cache.clear()
            self.exit()
