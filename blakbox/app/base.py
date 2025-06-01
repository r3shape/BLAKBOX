from .clock import BOXclock

from .inputs import BOXmouse
from .events import BOXevents
from .inputs import BOXkeyboard

from .window import BOXwindow

from blakbox.atom import BOXatom
from blakbox.log import BOXlogger

from blakbox.scene.base import BOXscene
from blakbox.resource.base import BOXresource

class BOXapplication(BOXatom):
    __slots__ = (
        "_name",
        "_scene",
        "_scenev",
        "_clock",
        "_resource",
        "_mouse",
        "_events",
        "_keyboard",
        "_window"
    )

    def __init__(
            self,
            name: str = "BOXapp",
            window_size: list[int] = [1280, 720]
    ) -> None:
        super().__init__()

        self._unfreeze()
        self._name: str = name
        self._scene: BOXscene = None
        self._scenev: list[BOXscene] = []
        self._clock: BOXclock = BOXclock()
        self._resource: BOXresource = BOXresource()
        self._mouse: BOXmouse = BOXmouse()
        self._events: BOXevents = BOXevents()
        self._keyboard: BOXkeyboard = BOXkeyboard()
        self._window: BOXwindow = BOXwindow(name, window_size)
        self._freeze()

        self.on_init()

    @property
    def name(self) -> str:
        return self._name

    @property
    def clock(self) -> BOXclock:
        return self._clock

    @property
    def resource(self) -> BOXresource:
        return self._resource

    @property
    def mouse(self) -> BOXmouse:
        return self._mouse

    @property
    def keyboard(self) -> BOXkeyboard:
        return self._keyboard

    @property
    def events(self) -> BOXevents:
        return self._events

    @property
    def window(self) -> BOXwindow:
        return self._window

    @property
    def scene(self) -> BOXscene:
        return self._scene

    def on_init(self) -> None:
        raise NotImplementedError
    
    def on_exit(self) -> None:
        raise NotImplementedError

    def add_scene(self, scene: BOXscene) -> int:
        index = len(self._scenev)
        if scene in self._scenev:
            return index - 1
        self._unfreeze()
        self._scenev.append(scene)
        self._freeze()
        return index
    
    def set_scene(self, index: int) -> None:
        if self._scene is not None:
            self._scene.on_exit()
        try:
            self._unfreeze()
            self._scene = self._scenev[index]
            self._freeze()
            self._scene.on_init()
        except IndexError as err:
            BOXlogger.error(f"Scene Not Found: (index){index} (err){err}")

    def rem_scene(self, index: int) -> None:
        try:
            scene = self._scenev.pop(index)
            if self.scene == scene:
                scene.on_exit()
                self._unfreeze()
                self.scene = None
                self._freeze()
        except IndexError as err:
            BOXlogger.error(f"Scene Not Found: (index){index} (err){err}")
    
    def run(self) -> None:
        while not self._events.quit:
            self._events.update()
            self._clock.update()
            self._window.clear()
            
            if self._scene is not None:
                self._scene.on_event()
                
                self._scene._physics.update(self._clock._dt)
                self._scene._world.update()
                self._scene.on_update()
                
                self._scene._camera.update(self._clock._dt)
                self._scene._renderer.update(self._clock._dt)
                self._scene._interface.update()
                
            self._clock.tick()
            self._window.flip()
        else:
            if self._scene is not None:
                self._scene.on_exit()
            self.on_exit()

