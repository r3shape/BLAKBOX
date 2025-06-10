from ...globals import pg, time
from ...atom import BOXatom, BOXprivate

class BOXclock(BOXatom):
    def __init__(self, target: float = 60.0) -> None:
        super().__init__()
        self.internal = pg.time.Clock()
        self.dt: float = 0.0
        self.fps: float = 0.0
        self.fpst: float = target
        self.now: float = time.time()
        self.last: float = time.time()
        self.start: float = time.time()

    @property
    def tick(self) -> int:
        return self.internal.tick(self.fpst)

    @BOXprivate
    def update(self) -> None:
        self.dt, self.last = time.time() - self.now, self.now
        self.fps = self.internal.get_fps()
        self.now = time.time()
