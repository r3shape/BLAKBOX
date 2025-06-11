from ....utils import add_v2, sub_v2, div_v2, mul_v2, damp_lin, norm_v2
from ....globals import pg, math
from ....atom import BOXatom

# ------------------------------------------------------------ #
class BOXobject(BOXatom):
    class flags:
        BOUNDED: int    = 1 << 0
        VISIBLE: int    = 1 << 1
        COLLISIONS: int = 1 << 2
        DYNAMIC: int    = 1 << 3
        GRAVITY: int    = 1 << 4
        DIRTY: int      = 1 << 5

    def __init__(
            self,
            tag: str = "BOXobject",
            mass: float = 50.0,
            speed: float = 100.0,
            size: list[int] = [8, 8],
            pos: list[float] = [0, 0],
            bounds: list[int] = [0, 0],
            color: list[int] = [0, 0, 0],
            flags: int = 0,
            ):
        super().__init__()
        self.tag: str = tag
        self.size: list[int] = size[:]
        self.color: list[int] = color[:]
        self.surface: pg.Surface = pg.Surface(size, pg.SRCALPHA)
        self.surface.fill(color)
        
        self.mass: float = mass
        self.speed: float = speed
        self.rotation: float = 0.0
        
        self.pos: list[int] = pos[:]                    # managed internally by BOXphysics
        self.last_pos: list[int] = pos[:]               # managed internally by BOXphysics

        self.vel: list[int] = [0, 0]
        self.bounds: list[int] = bounds[:]
        self.mvmt: list[float] = [0, 0, 0, 0]           # managed internally by BOXphysics
        self.collisions: list[bool] = [0, 0, 0, 0]      # managed internally by BOXphysics

        self.target_gap: float = 2.0
        self.target_pos: list[float] = None
        
        self.grid_query_size: list[int] = [1, 1]            # managed internally by BOXgrid
        self.grid_cell: list[int] = [0, 0]                  # managed internally by BOXgrid
        self.last_grid_cell: list[int] = [0, 0]             # managed internally by BOXgrid
        self.last_grid_region: list[int] = [0, 0]             # managed internally by BOXgrid
        self.grid_neighbors: list[list['BOXobject']] = []   # managed internally by BOXgrid

        self.set_flag(flags)

    @property
    def rect(self) -> pg.Rect:
        return pg.Rect(self.pos, self.size)

    @property
    def center(self) -> list[float]:
        return add_v2(self.pos, div_v2(self.size, 2))

    @property
    def direction(self) -> list[float]:
        return [(self.mvmt[3] - self.mvmt[2]), (self.mvmt[1] - self.mvmt[0])]
    
    @property
    def transform(self) -> list[float]:
        return add_v2(mul_v2([(self.mvmt[3] - self.mvmt[2]), (self.mvmt[1] - self.mvmt[0])], [self.speed, self.speed]), self.vel)

    @property
    def rotated(self) -> tuple[pg.Surface, pg.Rect]:
        rot_surf = pg.transform.rotate(self.surface, self.rotation)
        rot_rect = rot_surf.get_frect(center=self.center)
        return rot_surf, rot_rect

    def set_color(self, color: list[int], fill: bool = False) -> None:
        self.color = color
        if fill: self.surface.fill(color)

    def set_colorkey(self, key: list[int]) -> None:
        self.surface.set_colorkey(key)

    def set_vel(self, vx: float=None, vy: float = None) -> None:
        if vx is not None: self.vel[0] = vx
        if vy is not None: self.vel[1] = vy

    def move_to(self, target: list[float]) -> None:
        self.target_pos = target[:]

    def look_to(self, target: list[float]) -> None:
        d = norm_v2(sub_v2(target, self.pos))
        self.rotation = math.degrees(math.atan2(-d[1], d[0]))

    def move(self, left: bool=None, right: bool=None, up: bool=None, down: bool=None) -> None:
        self.mvmt[0] = up if up is not None else self.mvmt[0]
        self.mvmt[1] = down if down is not None else self.mvmt[1]
        self.mvmt[2] = left if left is not None else self.mvmt[2]
        self.mvmt[3] = right if right is not None else self.mvmt[3]
    
    def on_collide(self, obj: "BOXobject") -> None:         pass
    def on_collide_up(self, obj: "BOXobject") -> None:      pass
    def on_collide_down(self, obj: "BOXobject") -> None:    pass
    def on_collide_left(self, obj: "BOXobject") -> None:    pass
    def on_collide_right(self, obj: "BOXobject") -> None:   pass
# # ------------------------------------------------------------ #