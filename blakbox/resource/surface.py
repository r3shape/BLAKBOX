from .frame import BOXframe
from .base import BOXresource
from blakbox.globals import pg
from blakbox.utils import add_v2, div_v2

class BOXsurface(BOXframe):
    __slots__ = (
        "_filepath",
        "_pos",
        "_size",
        "_layout",
        "_rect",
        "_scale",
        "_color",
        "_color_key",
    )

    def __init__(
            self, resource: BOXresource,
            filepath: str,
            size: list[int],
            scale: list[int] = None,
            layout: list[int] = [1, 1],
            color: list[int] = [0, 0, 0],
            color_key: list[int] = None,
    ) -> None:
        super().__init__(resource, resource.load_surface(filepath, size, scale, layout, color, color_key))

        self._unfreeze()
        self._filepath: str = self.data[0]
        self._pos: list[int] = self.data[1]
        self._size: list[int] = self.data[2]
        self._layout: list[int] = self.data[3]
        self._rect: list[int] = self.data[4]
        self._scale: list[int] = self.data[5]
        self._color: list[int] = self.data[6]
        self._color_key: list[int] = self.data[7]
        self._freeze()

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
    def rect(self) -> pg.Rect:
        return self._rect
    
    @property
    def scale(self) -> list[int]:
        return self._scale
    
    @property
    def color(self) -> list[int]:
        return self._color
