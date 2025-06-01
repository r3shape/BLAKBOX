from blakbox.globals import os
from blakbox.atom import BOXatom
from blakbox.utils import scale_v2i

class BOXgrid(BOXatom):
    __slots__ = (
        "_size",
        "_area",
        "_data",
        "_cell_size",
        "_cell_area",
        "_cell_count"
    )
    def __init__(
            self,
            cell_size: int,
            cell_count: list[int]
    ) -> None:
        super().__init__()

        self._unfreeze()
        self._cell_size: int = int(cell_size)
        self._cell_area: int = self._cell_size * self._cell_size
        self._cell_count: list[int] = scale_v2i(cell_count[:], 1)
        
        self._size: list[int] = scale_v2i(cell_count[:], cell_size)
        self._area: int = self._size[0] * self._size[1]

        self._data: list[list[int]] = [None for cell in range(self._area)]
        self._freeze()
        
    @property
    def size(self) -> list[int]:
        return self._size

    @property
    def area(self) -> list[int]:
        return self._area

    @property
    def cell_size(self) -> list[int]:
        return self._cell_size

    @property
    def cell_count(self) -> list[int]:
        return self._cell_count
