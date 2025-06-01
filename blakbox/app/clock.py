from blakbox.globals import pg, time
from blakbox.atom import BOXatom

class BOXclock(BOXatom):
    __slots__ = (
        "_internal",
        "_dt",
        "_fps",
        "_fpst",
        "_now",
        "_last",
        "_start"
    )

    def __init__(self, target: float = 60.0) -> None:
        super().__init__()
        
        self._unfreeze()
        self._internal = pg.time.Clock()
        self._dt: float = 0.0
        self._fps: float = 0.0
        self._fpst: float = 60.0
        self._now: float = time.time()
        self._last: float = time.time()
        self._start: float = time.time()
        self._freeze()

    @property
    def dt(self) -> float:
        return self._dt
    
    @property
    def fps(self) -> float:
        return self._fps

    @property
    def now(self) -> float:
        return self._now

    @property
    def last(self) -> float:
        return self._last

    @property
    def start(self) -> float:
        return self._start

    def tick(self) -> int:
        return self._internal.tick(self._fpst)

    def update(self) -> None:
        self._unfreeze()
        self._dt, self._last = time.time() - self._now, self._now
        self._fps = self._internal.get_fps()
        self._now = time.time()
        self._freeze()
