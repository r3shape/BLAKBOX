from blakbox.atom import BOXprivate, BOXatom, BOXflag
from blakbox.utils import mul_v2, scale_v2, scale_v2i

import blakbox

class BOXcamera(BOXatom):
    __slots__ = (
        "_scene",
        "_window",
        "_speed",
        "_pos",
        "_dir",
        "_bounds"
    )

    def __init__(
            self,
            scene: blakbox.scene.base.BOXscene,
            pos: list[float], bounds: list[int]
    ) -> None:
        super().__init__()

        self._unfreeze()
        self._speed: int = 120
        self._pos: list[float] = pos[:]
        self._dir: list[int] = [0, 0, 0, 0]
        self._bounds: list[int] = scale_v2i(bounds[:], 1)
        self._scene: blakbox.scene.base.BOXscene = scene
        self._window: blakbox.app.window.BOXwindow = scene.app.window
        self._freeze()
        
    @property
    def scene(self):
        return self._scene

    @property
    def window(self):
        return self._window

    @property
    def speed(self) -> list[float]:
        return self._speed

    @property
    def x(self) -> float:
        return self._pos[0]

    @property
    def y(self) -> float:
        return self._pos[1]

    @property
    def pos(self) -> list[float]:
        return self._pos
    
    @property
    def dir(self) -> list[int]:
        return self._dir

    @property
    def vx(self) -> float:
        return (self._dir[3] - self._dir[2]) * self.speed

    @property
    def vy(self) -> float:
        return (self._dir[1] - self._dir[0]) * self.speed

    @property
    def vel(self) -> list[float]:
        return [self.vx, self.vy]

    def move(
            self,
            up: bool = None,
            down: bool = None,
            left: bool = None,
            right: bool = None
    ) -> None:
        if up:      self._dir[0] = up
        if down:    self._dir[1] = down
        if left:    self._dir[2] = left
        if right:   self._dir[3] = right

    @BOXprivate
    def update(self, dt: float) -> None:
        vel = self.vel
        if self.get_flag(BOXflag.BOUNDED):
            self._pos[0] = max(0, min(self._bounds[0], self._pos[0] + vel[0] * dt))
            self._pos[1] = max(0, min(self._bounds[1], self._pos[1] + vel[1] * dt))
        else:
            self._pos[0] += vel[0] * dt
            self._pos[1] += vel[1] * dt
        
        self._dir[0], self._dir[1], self._dir[2], self._dir[3] = 0, 0, 0, 0


