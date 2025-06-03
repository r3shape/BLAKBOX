from .frame import BOXframe
from .base import BOXresource, BOXresourceFlag
from blakbox.utils import add_v2, div_v2

class BOXobject(BOXframe):
    __slots__ = (
        "_pos",
        "_dir",
        "_size",
        "_speed",
    )

    def __init__(
        self, resource: BOXresource,
        pos: list[int],
        size: list[int],
        speed: float = 100.0
    ) -> None:
        super().__init__(resource, resource.load_object(pos, size, speed))
        
        self._unfreeze()
        self._pos: list[float]  = self.data[0]
        self._dir: list[float]  = self.data[1]
        self._size: list[float] = self.data[2]
        self._speed: float      = self.data[3]
        self._freeze()
        
    @property
    def size(self) -> list[int]:
        return self._size
    
    @property
    def speed(self) -> list[float]:
        return self._speed
    
    @speed.setter
    def speed(self, speed: float) -> None:
        self._unfreeze()
        self._speed = speed
        self._freeze()

    @property
    def pos(self) -> list[float]:
        return self._pos

    @property
    def x(self) -> float:
        return self._pos[0]

    @property
    def y(self) -> float:
        return self._pos[1]

    @property
    def dir(self) -> list[int]:
        return self._dir

    @property
    def center(self) -> list[float]:
        return add_v2(self._pos, div_v2(self._size, 2))

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

    def update(self, dt: float) -> None:
        vel = self.vel
        if self.get_flag(BOXresourceFlag.BOUNDED):
            self._pos[0] = max(0, min(self._bounds[0], self._pos[0] + vel[0] * dt))
            self._pos[1] = max(0, min(self._bounds[1], self._pos[1] + vel[1] * dt))
        else:
            self._pos[0] += vel[0] * dt
            self._pos[1] += vel[1] * dt
        
        self._dir[0], self._dir[1], self._dir[2], self._dir[3] = 0, 0, 0, 0

