from ...utils import mul_v2, div2_v2
from ...atom import BOXprivate, BOXatom
from ..scene.base import BOXscene
from ..resource import BOXobject

class BOXworld(BOXatom):
    def __init__(
            self,
            scene: BOXscene,
            node_size:  list[int] = [32, 32],
            chunk_size: list[int] = [4, 4],
            world_size: list[int] = [2, 2]
        ) -> None:
        super().__init__()

        self.node_size:  list[int] = node_size[:]                           # in pixels
        self.chunk_size: list[int] = chunk_size                             # in nodes
        self.world_size: list[int] = world_size                             # in chunks
        self.chunk_size_raw: list[int] = mul_v2(chunk_size, node_size)      # in pixels
        self.world_size_raw: list[int] = mul_v2(world_size, chunk_size)     # in pixels

        # world[(wx, wy)] -> dict[tuple, set[BOXobject]]
        # world[(wx, wy)][(cx, cy)] -> set[BOXobject]
        self.world: dict[dict[tuple, set[BOXobject]]] = {}

    def to_node_pos(self, pos: list[float]) -> tuple[int]:
        return tuple(map(int, mul_v2(div2_v2(pos, self.node_size), self.node_size)))

    def to_chunk_pos(self, pos: list[float]) -> tuple[int]:
        return tuple(map(int, mul_v2(div2_v2(pos, self.chunk_size), self.chunk_size)))

    def to_world_pos(self, pos: list[float]) -> tuple[int]:
        return tuple(map(int, mul_v2(div2_v2(pos, self.world_size), self.world_size)))
    
    @BOXprivate
    def update(self) -> None: pass
        