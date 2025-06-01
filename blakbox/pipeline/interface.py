from .render import BOXrenderer
from blakbox.atom import BOXprivate, BOXatom

from collections import namedtuple
import blakbox

class BOXinterfaceCommit(BOXatom):
    __slots__ = ("_surface", "pos")

    def __init__(self, surface: blakbox.resource.BOXsurface, pos: list[float]) -> None:
        super().__init__()
        self._unfreeze()
        self.surface: blakbox.resource.BOXsurface = surface
        self.pos: list[float] = pos
        self._freeze()

class BOXinterface(BOXrenderer):

    def __init__(
            self,
            scene: blakbox.scene.base.BOXscene
    ) -> None:
        super().__init__(scene)

        self._unfreeze()
        self._freeze()
        
    @property
    def scene(self):
        return self._scene

    def update(self) -> None: pass

