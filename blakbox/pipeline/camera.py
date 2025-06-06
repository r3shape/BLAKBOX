from ..globals import pg, random
from ..atom import BOXatom
from ..app.window import BOXwindow
from ..resource import BOXobject
from ..utils import add_v2, sub_v2, div_v2, scale_v2, scale_v2i

# ------------------------------------------------------------ #
class BOXcamera(BOXatom):
    class flags:
        DUAL_SNAP: int = 1 << 0

    def __init__(self, window: BOXwindow):
        super().__init__()
        self.window: BOXwindow = window
        self.bounds = window.display_size[:]
        self.viewport_size = window.display_size[:]
        self.viewport_scale = [
            window.screen_size[0] / self.viewport_size[0],
            window.screen_size[1] / self.viewport_size[1],
        ]

        self.speed = 100
        self.deadzone = 8
        self.zoom_min = 50

        self.pos = [0.0, 0.0]
        self.vel = [0.0, 0.0]

        self.shake_timer = 0.0
        self.shake_intensity = 0.0
        self.shake_offset = [0.0, 0.0]

        self.set_flag(BOXcamera.flags.DUAL_SNAP)

    @property
    def viewport(self) -> pg.Rect:
        return pg.Rect(self.pos, self.viewport_size)

    @property
    def center(self) -> list[float]:
        return add_v2(self.pos, div_v2(self.viewport_size, 2))

    @property
    def offset(self) -> list[int]:
        offset = scale_v2i(self.pos, -1)
        shake_i = scale_v2i(self.shake_offset, -1)
        return add_v2(offset, shake_i)

    def center_rect(self, size: list[int]) -> pg.Rect:
        return pg.Rect(
            sub_v2(add_v2(self.pos, div_v2(self.viewport_size, 2)), div_v2(size, 2)),
            size
        )

    def shake(self, intensity: float, duration: float) -> None:
        self.shake_intensity = intensity
        self.shake_timer = duration

    def pan(self, target: list[float]) -> None:
        cam_center = add_v2(self.pos, div_v2(self.viewport_size, 2))
        dx, dy = sub_v2(target, cam_center)
        dist = (dx * dx + dy * dy) ** 0.5
        if abs(dist) < self.deadzone: return
        self.vel[0] += dx
        self.vel[1] += dy

    def mod_viewport(self, delta: float):
        delta *= min(self.viewport_size) * 0.1
        aspect = self.window.screen_size[0] / self.window.screen_size[1]

        new_height = max(self.zoom_min, self.viewport_size[1] + delta)
        new_width = new_height * aspect

        if new_width > self.bounds[0]:
            new_width = self.bounds[0]
            new_height = new_width / aspect

        self.viewport_size = [new_width, new_height]
        return self.viewport_size

    def box_mode(self, target_pos: list[float], target_size: list[float], box_size: list[int] = [132, 132]):
        target_center = add_v2(target_pos, div_v2(target_size, 2))
        cam_center = add_v2(self.pos, div_v2(self.viewport_size, 2))

        box_half = div_v2(box_size, 2)
        dx, dy = sub_v2(target_center, cam_center)
        dist = (dx * dx + dy * dy) ** 0.5

        if abs(dist) < self.deadzone: return

        if self.get_flag(BOXcamera.flags.DUAL_SNAP):
            if abs(dx) > box_half[0]:
                self.vel[0] += dx * (self.speed * 0.001) * 2
            if abs(dy) > box_half[1]:
                self.vel[1] += dy * (self.speed * 0.001) * 2
        else:
            if abs(dx) > box_half[0]:
                self.vel[0] += dx * (self.speed * 0.001)
            if abs(dy) > box_half[1]:
                self.vel[1] += dy * (self.speed * 0.001)

    def snap_mode(self, target_pos: list[float], target_size: list[float]):
        target_center = add_v2(target_pos, div_v2(target_size, 2))
        cam_center = add_v2(self.pos, div_v2(self.viewport_size, 2))

        dx, dy = sub_v2(target_center, cam_center)
        dist = (dx * dx + dy * dy) ** 0.5
        
        if abs(dist) < self.deadzone: return
        
        if self.get_flag(BOXcamera.flags.DUAL_SNAP):
            if abs(dist) > target_size[0] or abs(dist) > target_size[1]:
                self.vel[0] += dx * (self.speed * 0.001) * 2
                self.vel[1] += dy * (self.speed * 0.001) * 2
        else:
            self.vel[0] += dx * (self.speed * 0.001)
            self.vel[1] += dy * (self.speed * 0.001)

    def update(self, dt: float):
        self.viewport_scale = [
            self.window.screen_size[0] / self.viewport_size[0],
            self.window.screen_size[1] / self.viewport_size[1]
        ]

        self.pos[0] += self.vel[0] * dt
        self.pos[1] += self.vel[1] * dt

        max_x = self.bounds[0] - self.viewport_size[0]
        max_y = self.bounds[1] - self.viewport_size[1]
        self.pos[0] = max(0, min(max_x, self.pos[0]))
        self.pos[1] = max(0, min(max_y, self.pos[1]))

        self.vel[0] *= 0.85
        self.vel[1] *= 0.85

        if self.shake_timer > 0:
            self.shake_offset = [
                random.uniform(-1, 1) * self.shake_intensity,
                random.uniform(-1, 1) * self.shake_intensity
            ]
            self.shake_timer -= dt
        else:
            self.shake_offset = [0.0, 0.0]
# ------------------------------------------------------------ #