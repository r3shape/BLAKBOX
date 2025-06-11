from ...atom import BOXatom
from ...utils import add_v2, sub_v2, scale_v2, div_v2, div2_v2, damp_lin

from ..scene.grid import BOXgrid
from ..scene.tilemap import BOXtilemap
from ..resource.game.object import BOXobject

from ..app.window import BOXwindow
from ..pipeline.camera import BOXcamera

class BOXphysics(BOXatom):
    class flags:
        COLLISIONS: int     = 1 << 0
        GRAVITY: int        = 1 << 1
        FRICTION_X: int     = 1 << 2
        FRICTION_Y: int     = 1 << 3

    def __init__(self, tilemap, world):
        super().__init__()
        self.world = world
        self.grid: BOXgrid = tilemap.grid
        self.tilemap: BOXtilemap = tilemap
        
        self.objects: int = 0
        self.gravity: float = 9.8
        self.friction: float = 9.8
        self.query_size: list[int] = [1, 1]

        self.set_flag(self.flags.GRAVITY | self.flags.FRICTION_X | self.flags.COLLISIONS)

    def grid_query(self, obj: BOXobject) -> list[list[BOXobject]]:
        if not obj.get_flag(obj.flags.COLLISIONS): return []
        return self.grid.get_region(obj.grid_query_size, obj.pos)

    def apply_gravity(self, obj: BOXobject, dt: float) -> None:
        if obj.collisions[1]:
            obj.vel[1] = 0
            return
        if not obj.get_flag(obj.flags.GRAVITY): return
        if not self.get_flag(self.flags.GRAVITY): return
        obj.vel[1] += (100/obj.mass) * self.gravity * dt

    def apply_friction(self, obj: BOXobject, dt: float) -> None:
        if self.get_flag(self.flags.FRICTION_X):
            obj.vel[0] = damp_lin(obj.vel[0], self.friction, 4, dt)
        if self.get_flag(self.flags.FRICTION_Y):
            obj.vel[1] = damp_lin(obj.vel[1], self.friction, 4, dt)

    def x_aabb(self, obj: BOXobject, neighbors: list[BOXobject]) -> bool:
        if not obj.get_flag(obj.flags.COLLISIONS): return       # per-object collision flag
        if not self.get_flag(self.flags.COLLISIONS): return     # pipeline collision flag
        collider = obj.rect
        transform = obj.transform
        for o in neighbors:
            if o == obj: continue
            if not o: continue
            if collider.colliderect(o.rect):
                if transform[0] < 0:    # left collisions
                    collider.left = o.rect.right
                    obj.mvmt[2] = 0
                    obj.collisions[2] = 1
                    obj.on_collide(o)
                    obj.on_collide_left(o)
                elif transform[0] > 0:    # right collisions
                    collider.right = o.rect.left
                    obj.mvmt[3] = 0
                    obj.collisions[3] = 1
                    obj.on_collide(o)
                    obj.on_collide_right(o)
                obj.pos[0] = collider.x

    def y_aabb(self, obj: BOXobject, neighbors: list[BOXobject]) -> bool:
        if not obj.get_flag(obj.flags.COLLISIONS): return       # per-object collision flag
        if not self.get_flag(self.flags.COLLISIONS): return     # pipeline collision flag
        collider = obj.rect
        transform = obj.transform
        for o in neighbors:
            if o == obj: continue
            if not o: continue
            if collider.colliderect(o.rect):
                if transform[1] < 0:    # top collisions
                    collider.top = o.rect.bottom
                    obj.vel[1] = 0
                    obj.mvmt[0] = 0
                    obj.collisions[0] = 1
                    obj.on_collide(o)
                    obj.on_collide_up(o)
                elif transform[1] > 0:    # bottom collisions
                    collider.bottom = o.rect.top
                    obj.vel[1] = 0
                    obj.mvmt[1] = 0
                    obj.collisions[1] = 1
                    obj.on_collide(o)
                    obj.on_collide_down(o)
                obj.pos[1] = collider.y

    def update(self, dt: float) -> None:
        self.objects = len(self.grid.all)
        for o in self.grid.all:
            if not o.get_flag(o.flags.DYNAMIC): continue
            neighbors = o.grid_neighbors
            o.collisions = [0, 0, 0, 0]
            transform = o.transform
            
            # handle BOXobject.move_to()
            if o.target_pos:
                dx = o.target_pos[0] - o.center[0]
                dy = o.target_pos[1] - o.center[1]
                dist = (dx * dx + dy * dy) ** 0.5
                if dist < o.target_gap:
                    o.target_pos = None
                    o.mvmt = [0, 0, 0, 0]
                else:
                    dir_x = dx / dist
                    dir_y = dy / dist
                    o.vel[0] = dir_x * o.speed
                    o.vel[1] = dir_y * o.speed
            
            if o.get_flag(o.flags.BOUNDED):
                o.pos[0] = max(0, min(o.bounds[0] - o.size[0], o.pos[0] + transform[0] * dt))
                self.apply_friction(o, dt)
                if self.x_aabb(o, neighbors):
                    o.vel[0] = 0

                o.pos[1] = max(0, min(o.bounds[1] - o.size[1], o.pos[1] + transform[1] * dt))
                self.apply_gravity(o, dt)
                if self.y_aabb(o, neighbors):
                    o.vel[1] = 0
            else:
                o.pos[0] += transform[0] * dt
                self.apply_friction(o, dt)
                if self.x_aabb(o, neighbors):
                    o.vel[0] = 0

                o.pos[1] += transform[1] * dt
                if self.y_aabb(o, neighbors):
                    o.vel[1] = 0
                self.apply_gravity(o, dt)
            
            o.last_pos = o.pos[:]
