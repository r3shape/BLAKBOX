from ..globals import pg
from ..atom import BOXatom
from ..utils import equal_arrays
from ..app.window import BOXwindow
from ..pipeline.camera import BOXcamera
from ..resource.object import BOXobject
from ..resource.particle import BOXparticles

# ------------------------------------------------------------ #
class BOXrenderer(BOXatom):
    class flags:
        Y_SORT: int = 1 << 0
        DEBUG_OBJECT: int = 1 << 1
        DEBUG_CAMERA: int = 1 << 2
        DEBUG_TILEMAP: int = 1 << 3


    def __init__(self, scene, window: BOXwindow, camera: BOXcamera) -> None:
        super().__init__()
        self.scene = scene
        self.window: BOXwindow = window
        self.camera: BOXcamera = camera
        self.particles: BOXparticles = BOXparticles()
        
        self.blits: int = 0
        self.blitv: list = []

        self.target = pg.Surface(self.camera.viewport_size)
        self.last_viewport_size: list[int] = self.camera.viewport_size

        self.debug_object_color: list[int] = [0, 255, 0]
        self.debug_camera_color: list[int] = [255, 0, 0]
        self.debug_tilemap_color: list[int] = [50, 50, 50]

        def _particles_001(x, y, lifetime, size, color) -> None:
            self.window.draw_circle(center=(int(x), int(y)), radius=int(size), color=color, width=1)
        self.particles_001 = _particles_001

    """ RENDER CALL"""
    def commitv(self, objects: list[BOXobject]) -> None:
        if not isinstance(objects, list): return
        for object in objects: self.commit(object)

    def commit(self, object: BOXobject, surface: pg.Surface = None) -> None:
        if not isinstance(object, BOXobject): return
        if self.blits + 1 > 4096: return
        if object is None: return

        # frustum culling
        if object.pos[0] + object.size[0] < self.camera.pos[0] or object.pos[0] > self.camera.pos[0] + self.camera.viewport_size[0]\
        or object.pos[1] + object.size[1] < self.camera.pos[1] or object.pos[1] > self.camera.pos[1] + self.camera.viewport_size[1]:
            object.rem_flag(object.flags.VISIBLE)
            return
        else: object.set_flag(object.flags.VISIBLE)

        if surface is None:
            surf, rect = object.rotated
        else:
            surf = pg.transform.rotate(surface, object.rotation)
            rect = surf.get_frect(center=object.center)

        self.blitv.append([object.pos[1], surf, rect, object.pos])
        self.blits += 1

    """ DEBUG RENDERING """
    def debug_object(self, rect: pg.Rect) -> None:
        self.window.blitr(rect, color=self.debug_object_color, width=1)

    def debug_camera(self) -> None:
        self.window.blitr(self.camera.viewport, color=self.debug_camera_color, width=1)
        self.window.blitr(self.camera.center_rect([10, 10]), color=self.debug_camera_color, width=1)

    def debug_tilemap(self) -> None:
        tile_size = self.scene.tilemap.tile_size
        grid_size = self.scene.tilemap.grid_size
        
        start = [0, 0]
        end = [(start[0] + (grid_size[0] * tile_size[0])) // tile_size[0],
               (start[1] + (grid_size[1] * tile_size[1])) // tile_size[1]]
        
        for gx in range(int(start[0]), int(end[0])):
            x = gx * tile_size[0]
            pg.draw.line(self.window.display, self.debug_tilemap_color, [x, start[1] * tile_size[1]], [x, end[1] * tile_size[1]], 1)
        
        for gy in range(int(start[1]), int(end[1])):
            y = gy * tile_size[1]
            pg.draw.line(self.window.display, self.debug_tilemap_color, [start[0] * tile_size[0], y], [end[0] * tile_size[0], y], 1)

    """ RENDERING """
    def flush(self) -> None:
        self.target = pg.Surface(self.camera.viewport_size)
        self.target.fill(self.window.clear_color)
        self.window.clear()
        
        if self.get_flag(self.flags.DEBUG_TILEMAP): self.debug_tilemap()

        
        if self.get_flag(self.flags.Y_SORT):
            self.blitv.sort(key=lambda blit: blit.pop(0))
        else:
            [blit.pop(0) for blit in self.blitv]
        for _ in range(self.blits):
            surf, rect, pos = self.blitv.pop(0)
            self.window.blits(surf, pos, rect=rect)
            if self.get_flag(self.flags.DEBUG_OBJECT): self.debug_object(rect)
        self.blits = 0

        self.particles.render(self.particles_001)

        if self.get_flag(self.flags.DEBUG_CAMERA): self.debug_camera()

        self.target.blit(self.window.display, self.camera.offset)
        self.window.screen.blit(dest=[0, 0], source=pg.transform.scale(self.target, self.window.screen_size))
# ------------------------------------------------------------ #
