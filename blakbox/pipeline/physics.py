from ..atom import BOXatom
from ..utils import add_v2, sub_v2, scale_v2, div_v2, div2_v2

from ..scene.grid import BOXgrid
from ..scene.tilemap import BOXtilemap
from ..resource.object import BOXobject

from ..app.window import BOXwindow
from ..pipeline.camera import BOXcamera

class BOXphysics(BOXatom):
    def __init__(self, tilemap):
        super().__init__()
        self.grid: BOXgrid = tilemap.grid
        self.tilemap: BOXtilemap = tilemap
        self.objects: int = 0
        self.gravity: float = 9.8
        self.friction: float = 9.8
        self.query_size: list[int] = [1, 1]

    def grid_query(self, object: BOXobject) -> list[list[BOXobject]]:
        return self.grid.get_region(self.query_size, object.pos)

    def apply_gravity(self, object: BOXobject) -> None: ...
    def apply_friction(self, object: BOXobject) -> None: ...

    def x_aabb(self, object: BOXobject, against: list[BOXobject]) -> bool:
        collider = object.rect
        transform = object.transform
        for o in against:
            if not o: continue
            if o == object: continue
            if collider.colliderect(o.rect):
                if transform[0] < 0:
                    collider.left = o.rect.right
                    object.mvmt[2] = 0
                    object.collisions[2] = 1
                    object.on_collide(o)
                    object.on_collide_left(o)
                if transform[0] > 0:
                    collider.right = o.rect.left
                    object.mvmt[3] = 0
                    object.collisions[3] = 1
                    object.on_collide(o)
                    object.on_collide_right(o)
                object.pos[0] = collider.x

    def y_aabb(self, object: BOXobject, against: list[BOXobject]) -> bool: ...

    def update(self, dt: float) -> None:
        for o in self.grid.all:
            transform = o.transform
            cells = self.grid_query(o)
            print(cells)
            

