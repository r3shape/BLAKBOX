from blakbox.globals import pg
from blakbox.atom import BOXatom

class BOXevents(BOXatom):
    __slots__ = (
        "_quit",
        "_mouse",
        "_keyboard",
        "_mouse_old",
        "_keyboard_old",
        "_mouse_wheel_up",
        "_mouse_wheel_down"
    )

    def __init__(self) -> None:
        super().__init__()

        self._unfreeze()
        self._quit: bool=False

        self._keyboard = {}
        self._keyboard_old = {}

        self._mouse = {}
        self._mouse_old = {}
        self._mouse_wheel_up: bool=False
        self._mouse_wheel_down: bool=False
        self._freeze()

    @property
    def quit(self) -> bool:
        return self._quit

    def key_held(self, key):
        return self._keyboard.get(key, False)
    
    def key_pressed(self, key):
        return self._keyboard.get(key, False) and not self._keyboard_old.get(key, False)
        
    def mouse_held(self, button:int):
        return self._mouse.get(button, False)
    
    def mouse_pressed(self, button):
        return self._mouse.get(button, False) and not self._mouse_old.get(button, False)

    def update(self) -> int:
        self._unfreeze()
        self._mouse_wheel_up = False
        self._mouse_wheel_down = False
        self._mouse_old = self._mouse.copy()
        self._keyboard_old = self._keyboard.copy()
        
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_F12):
                self._quit = True
            match event.type:
                case pg.KEYUP:
                    self._keyboard[event.key] = False
                case pg.KEYDOWN:
                    self._keyboard[event.key] = True
                case pg.MOUSEBUTTONUP:
                    self._mouse[event.button] = False
                case pg.MOUSEBUTTONDOWN:
                    self._mouse[event.button] = True
                    if event.button == 4:
                        self._mouse_wheel_up = True
                    if event.button == 5:
                        self._mouse_wheel_down = True
        self._freeze()