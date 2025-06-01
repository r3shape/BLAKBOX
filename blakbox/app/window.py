from blakbox.globals import pg
from blakbox.atom import BOXatom
from blakbox.utils import scale_v2i, scale_v3i

class BOXwindow(BOXatom):
    __slots__ = (
        "_size",
        "_title",
        "_color",
        "_screen"
    )

    def __init__(
            self,
            title: str,
            size: list[int],
            color: list[int] = [10, 10, 10]
    ) -> None:
        super().__init__()

        self._unfreeze()
        self._title: str = title
        self._size: list[int] = scale_v2i(size[:], 1)
        self._color: list[int] = scale_v3i(color[:], 1)
        self._screen: pg.Surface = pg.display.set_mode(size[:])
        self._freeze()
        
    @property
    def title(self) -> str:
        return self._title
    
    @property
    def size(self) -> list[int]:
        return self._size

    @property
    def color(self) -> list[int]:
        return self._color
    
    @color.setter
    def color(self, color: list[int]) -> None:
        self._color = scale_v3i(color, 1)

    @property
    def screen(self) -> pg.Surface:
        return self._screen
    
    def clear(self) -> None:
        self._screen.fill(self._color)

    def flip(self) -> None:
        pg.display.flip()
