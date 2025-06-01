from blakbox.globals import pg
from blakbox.atom import BOXatom
from blakbox.log import BOXlogger

from .base import BOXresource
from .base import BOXhandle

class BOXframe(BOXatom):
    __slots__ = (
        "_data",
        "_resource",
        "_handle",
        "_frozen"
    )

    def __init__(
            self,
            resource: BOXresource,
            handle: BOXhandle,
    ) -> None:
        super().__init__()

        self._unfreeze()
        self._resource: BOXresource = resource
        self._handle: BOXhandle = handle
        self._data: list = self._resource.get(self._handle)
        self._freeze()
        
    @property
    def data(self) -> list:
        return self._data

    @property
    def resource(self) -> BOXresource:
        return self._resource

    @property
    def handle(self) -> BOXhandle:
        return self._handle

    def destroy(self) -> None:
        self._resource.rem(self._handle)
