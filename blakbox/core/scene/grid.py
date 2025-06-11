from ...globals import pg, math
from ...log import BOXlogger
from ...utils import div2_v2i, div_v2, mul_v2, add_v2
from ...atom import BOXprivate, BOXatom

from ..resource import BOXobject

class BOXgrid(BOXatom):
    def __init__(
            self,
            cell_size: list[int],
            grid_size: list[int]
        ) -> None:
        super().__init__()
        self.all: list[BOXobject] = []
        
        self.grid_width: int = grid_size[0]
        self.grid_height: int = grid_size[1]
        self.grid: dict[tuple[int, int], list[BOXobject]] = {}
        self.grid_size: list[int] = mul_v2(cell_size, grid_size)
        
        self.cell_width: int = cell_size[0]
        self.cell_height: int = cell_size[1]
        self.cell_size: list[int] = cell_size
        self.cell_area: int = self.cell_width * self.cell_height

    @BOXprivate
    def _gen_object_region(self, obj: BOXobject) -> list[tuple[int, int]]:
        tl = obj.pos
        br = add_v2(obj.pos, obj.size)
        gx0, gy0 = map(int, div2_v2i(tl, self.cell_size))
        gx1, gy1 = map(int, div2_v2i(br, self.cell_size))

        region = []
        for x in range(gx0, gx1 + 1):
            for y in range(gy0, gy1 + 1):
                region.append((x, y))
        return region

    @BOXprivate
    def _gen_region(self, size: list[int], pos: list[int]) -> list[tuple[int, int]]:
        cx, cy = map(int, div2_v2i(pos, self.cell_size))
        region = []
        for x in range(cx - size[0], cx + size[0] + 1):
            for y in range(cy - size[1], cy + size[1] + 1):
                region.append((x, y))
        return region

    def to_grid_pos(self, pos: list[float]) -> tuple[int, int] | None:
        gx, gy = map(int, div_v2(pos, self.cell_width))
        if gx < 0 or gy < 0 or gx > self.grid_width or gy > self.grid_height:
            return None
        return (gx, gy)

    def from_grid_pos(self, cell: tuple[int, int]) -> list[int]:
        return [cell[0] * self.cell_width, cell[1] * self.cell_height]

    def get(self, pos: list[float]) -> list:
        grid_pos = self.to_grid_pos(pos)
        if grid_pos is None:
            return []
        return self.grid.get(grid_pos, [])

    def rem(self, obj: BOXobject) -> None:
        regions = self._gen_object_region(obj)
        for gx, gy in regions:
            cell = self.grid.get((gx, gy))
            if cell and obj in cell:
                cell.remove(obj)
                if not cell:
                    del self.grid[(gx, gy)]
        if obj in self.all:
            self.all.remove(obj)

    def set(self, obj: BOXobject) -> None:
        regions = self._gen_object_region(obj)
        for gx, gy in regions:
            cell = self.grid.setdefault((gx, gy), [])
            if obj not in cell:
                obj.grid_query_size = [
                    math.ceil(obj.size[0] / self.cell_size[0]),
                    math.ceil(obj.size[1] / self.cell_size[1])
                ]
                cell.append(obj)
        if obj not in self.all:
            self.all.append(obj)

    def setv(self, objects: list[BOXobject]) -> None:
        if not isinstance(objects, list):
            return
        for obj in objects:
            if not obj:
                continue
            self.set(obj)

    def get_region(self, size: list[int], pos: list[int]) -> list[list[BOXobject]]:
        region = self._gen_region(size, pos)
        if not region:
            return []
        cells = []
        for gx, gy in region:
            cell = self.grid.get((gx, gy))
            if cell:
                cells.append(cell)
        return cells

    def rem_region(self, size: list[int], pos: list[int]) -> None:
        region = self._gen_region(size, pos)
        for gx, gy in region:
            if (gx, gy) in self.grid:
                del self.grid[(gx, gy)]

    @BOXprivate
    def update(self) -> None:
        for obj in self.all:
            obj.last_grid_cell = obj.grid_cell[:]
            obj.grid_cell = self.to_grid_pos(obj.pos)

            if obj.grid_cell is None\
            or obj.last_grid_cell is None:
                obj.grid_cell = [-999, -999]
                continue
                
            if obj.grid_cell[0] != obj.last_grid_cell[0]\
            or obj.grid_cell[1] != obj.last_grid_cell[1]:
                obj.set_flag(obj.flags.DIRTY)
            else:
                obj.rem_flag(obj.flags.DIRTY)
                continue

            new_region = set(self._gen_object_region(obj))
            last_region = getattr(obj, 'last_region', set())

            if new_region != last_region:
                for gx, gy in last_region:
                    cell = self.grid.get((gx, gy))
                    if cell and obj in cell:
                        cell.remove(obj)
                        if not cell:
                            del self.grid[(gx, gy)]
                for gx, gy in new_region:
                    cell = self.grid.setdefault((gx, gy), [])
                    if obj not in cell:
                        cell.append(obj)

                obj.last_region = new_region

                obj.grid_neighbors = []
                for cell in self.get_region(obj.grid_query_size, obj.pos):
                    obj.grid_neighbors.extend(cell)
