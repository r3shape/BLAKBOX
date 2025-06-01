from blakbox.globals import pg
from blakbox.utils import sub_v2
from blakbox.atom import BOXprivate, BOXatom

from collections import namedtuple
import blakbox

class BOXrenderCommit(BOXatom):
    __slots__ = ("object", "surface")

    def __init__(self, surface: blakbox.resource.BOXsurface, object: blakbox.resource.BOXobject):
        super().__init__()
        self._unfreeze()
        self.surface: blakbox.resource.BOXsurface = surface
        self.object: blakbox.resource.BOXobject = object
        self._freeze()

class BOXrenderer(BOXatom):
    __slots__ = (
        "_commits",
        "_commitv",
        "_clip_range",
        "_scene",
        "_resource",
        "_window",
        "_camera",
    )

    class _commit_type:
        surface: int = (1 << 0)
        object: int = (1 << 1)

    def __init__(
            self,
            scene: blakbox.scene.base.BOXscene
    ) -> None:
        super().__init__()

        self._unfreeze()
        self._commits: int = 0
        self._commitv: list[int] = []
        self._clip_range: list[int] = [1, 1]
        self._scene: blakbox.scene.base.BOXscene = scene
        self._resource: blakbox.resource.base.BOXresource = scene._resource
        self._window: blakbox.app.window.BOXwindow = scene.app.window
        self._camera: blakbox.pipeline.camera.BOXcamera = scene._camera
        self._freeze()
        
    @property
    def scene(self):
        return self._scene

    @property
    def resource(self):
        return self._resource
    
    @property
    def window(self):
        return self._window
    
    @property
    def camera(self):
        return self._camera

    @property
    def commits(self) -> int:
        return self._commits

    @property
    def clip_range(self) -> list[int]:
        return self._clip_range
    
    def commit(self, commit: BOXrenderCommit) -> None:
        if self._commits + 1 >= 4096: return
        if not isinstance(commit.object, blakbox.resource.BOXobject): return
        if not isinstance(commit.surface, (blakbox.resource.BOXsurface, blakbox.resource.BOXsurfarray)): return

        x, y = commit.object.pos
        w, h = commit.object.size

        # screen-space clipping
        cx, cy = self._clip_range
        if x + w <= cx or x >= self._window._size[0] - cx\
        or y + h <= cy or y >= self._window._size[1] - cy:
            return

        commit = [commit.object, commit.surface]

        self._unfreeze()
        self._commitv.append(commit)
        self._commits += 1
        self._freeze()

    @BOXprivate
    def update(self, dt: float) -> None:
        self._window.clear()

        while self._commits:
            self._unfreeze()
            object, surf = self._commitv.pop(0)
            getattr(surf, "update", lambda dt: dt)(dt)

            frame = getattr(surf, "frame", None)
            if frame is None:
                rect = surf.rect
            else:
                rect = pg.Rect(frame, surf.size)

            self._window.screen.blit(self._resource._atlas, sub_v2(object.pos, self._camera.pos), rect)            
            self._commits -= 1
            self._freeze()

