from .frame import BOXframe
from blakbox.atom import BOXprivate
from .base import BOXresource, BOXresourceFlag
from blakbox.globals import pg
from blakbox.utils import add_v2, div_v2

import blakbox

class BOXsurfarray(BOXframe):
    __slots__ = (
        "_filepath",
        "_pos",
        "_size",
        "_rect",
        "_layout",
        "_count",
        "_index",
        "_timer",
        "_speed",
        "_scale",
        "_color",
        "_color_key",
    )
    def __init__(
            self, resource: BOXresource,
            filepath: str,
            size: list[int],
            layout: list[int],
            loop: bool=True,
            speed: float=5.0,
            scale: list[int] = [1, 1],
            color: list[int] = [0, 0, 0],
            color_key: list[int] = None,
        ) -> None:
        super().__init__(resource, resource.load_surfarray(filepath, size, layout, speed, scale, color, color_key))
        
        self._unfreeze()
        self._index: int = 0
        self._timer: float = 0.0
        self._filepath: str = self.data[0]
        self._pos: list[int] = self.data[1]
        self._size: list[int] = self.data[2]
        self._rect: list[int] = self.data[3]
        self._layout: list[int] = self.data[4]
        self._speed: float = 1 / self.data[5]
        self._scale: list[int] = self.data[6]
        self._color: list[int] = self.data[7]
        self._color_key: list[int] = self.data[8]
        self._count: int = self._layout[0] * self._layout[1]
        if loop: self.set_flag(BOXresourceFlag.LOOP)
        self._freeze()
    
    @property
    def count(self) -> int:
        return self._count
    
    @property
    def index(self) -> int:
        return self._index

    @property
    def timer(self) -> float:
        return self._timer

    @property
    def pos(self) -> list[int]:
        return self._pos

    @property
    def size(self) -> list[int]:
        return self._size

    @property
    def layout(self) -> list[int]:
        return self._layout

    @property
    def speed(self) ->float:
        return self._speed
    
    @property
    def rect(self) -> pg.Rect:
        return self._rect
    
    @property
    def scale(self) -> list[int]:
        return self._scale
    
    @property
    def color(self) -> list[int]:
        return self._color

    @property
    def frame(self) -> list[int]:
        c, r = self._layout
        frame_x = (self._index % c) * self._size[0]
        frame_y = (self._index // c) * self._size[1]
        return [frame_x, frame_y]

    def reset(self) -> None:
        self._unfreeze()
        self._timer = 0.0
        self._index = 0
        self._done = False
        self._freeze()

    @BOXprivate
    def update(self, dt: float) -> None:
        if self.get_flag(BOXresourceFlag.DONE): return
        
        self._unfreeze()
        self._timer += dt
        if self._timer >= self._speed:
            self._timer = 0
            self._index += 1
        
            if self._index >= self._count:
                if self.get_flag(BOXresourceFlag.LOOP):
                    self._index = 0
                else:
                    self._index = self._count - 1
                    self.set_flag(BOXresourceFlag.DONE)
        self._freeze()
