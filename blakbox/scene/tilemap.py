from ..log import BOXlogger
from ..atom import BOXprivate, BOXatom
from ..globals import os, pg, json, random
from ..utils import div2_v2i, mul_v2, rel_path, load_surface_array

from .grid import BOXgrid
from ..resource import BOXobject

class BOXtilemap(BOXatom):
    def __init__(
            self, scene,
            tile_size: list[int],
            grid_size: list[int],
            grid_color: list[int] = [50, 50, 50]
        ) -> None:
        self._config(scene, tile_size, grid_size, grid_color)

    @BOXprivate    
    def _config(self,scene,
            tile_size: list[int],
            grid_size: list[int],
            grid_color: list[int] = [50, 50, 50]
        ) -> None:
        self.scene = scene
        self.grid: BOXgrid = BOXgrid(tile_size, grid_size)  # spatial partitioning (tracks dynamic/static objects using BOXobject.grid_cell field)

        self.tile_size: list[int] = tile_size[:]                            # in pixels
        self.grid_size: list[int] = grid_size[:]                            # in tiles
        self.grid_size_raw: list[int] = mul_v2(grid_size, tile_size)        # in pixels
        
        self.grid_color: list[int] = grid_color[:]

        self.surface = pg.Surface(self.grid_size_raw, pg.SRCALPHA)
        self.surface.set_colorkey([1, 1, 1])
        self.surface.fill([1, 1, 1])
        
        self._blank = pg.Surface(self.tile_size, pg.SRCALPHA)
        self._blank.set_colorkey([1, 1, 1])
        self._blank.fill([1, 1, 1])

        self.tilesets: list[list[str, pg.Surface]] = []

        # self.layers[layer][0] = tile data layer
        # self.layers[layer][1] = tile object layer
        self.layers: dict[str, list] = {
            "bg": [[None for _ in range(grid_size[0] * grid_size[1])] for _ in range(2)],
            "fg": [[None for _ in range(grid_size[0] * grid_size[1])] for _ in range(2)],
            "mg":  [[None for _ in range(grid_size[0] * grid_size[1])] for _ in range(2)]
        }

    @BOXprivate    
    def _render_grid(self) -> None:
        start = [0, 0]
        end = [(self.grid_size[0] * self.tile_size[0]) // self.tile_size[0],
               (self.grid_size[1] * self.tile_size[1]) // self.tile_size[1]]
        
        for gx in range(int(start[0]), int(end[0])):
            x = gx * self.tile_size[0]
            pg.draw.line(self.surface, self.grid_color, [x, start[1] * self.tile_size[0]], [x, end[1] * self.tile_size[0]], 1)
        
        for gy in range(int(start[1]), int(end[1])):
            y = gy * self.tile_size[1]
            pg.draw.line(self.surface, self.grid_color, [start[0] * self.tile_size[1], y], [end[0] * self.tile_size[1], y], 1)

    @BOXprivate    
    def _gen_region(self, size:list[int], pos:list[int]) -> list[list[int]]:
        region = []
        cx, cy = map(int, div2_v2i(pos, self.tile_size))
        for x in range(cx - size[0], (cx + size[0]) + 1):
            for y in range(cy - size[1], (cy + size[1]) + 1):
                region.append([x, y])
        return region


    """ TILE OBJECT """
    def all_tiles(self, layer:str) -> list[BOXobject]:
        return [tile for tile in self.layers[layer][1] if tile]

    def set_tile(self, layer: str, pos: list[int], tile: int, tileset: int) -> None:
        gx, gy = div2_v2i(pos, self.tile_size)
        if tile < 0 or tileset < 0 or tileset >= len(self.tilesets):
            BOXlogger.error(f"[BOXtilemap] failed to set tile: (layer){layer} (tile){tile} (tileset){tileset} (pos){[gx, gy]}")
            BOXlogger.error(f"[BOXtilemap] tile/tileset index out of range: (tile){tile} (tileset){tileset}")
            return
        
        if not self.layers.get(layer, False):
            BOXlogger.error(f"[BOXtilemap] tilemap layer not found: (layer){layer}")
            return
        
        if gx < 0 or gy < 0 or gx >= self.grid_size[0] or gy >= self.grid_size[1]:
            BOXlogger.error(f"[BOXtilemap] failed to set tile: (layer){layer} (tile){tile} (tileset){tileset} (pos){[gx, gy]}")
            BOXlogger.error(f"[BOXtilemap] tile pos out of range: (pos){[gx, gy]} (grid){self.grid_size}")
            return

        index = int(gy * self.tile_size[0] + gx)
        if index < 0 or index >= len(self.layers[layer][1]):
            BOXlogger.error(f"[BOXtilemap] failed to set tile: (layer){layer} (tile){tile} (tileset){tileset} (pos){[gx, gy]}")
            BOXlogger.error(f"[BOXtilemap] data index out of range: (index){index} (len){len(self.layers[layer][1])}")
            return
        
        if self.layers[layer][1][index] is not None:
            BOXlogger.warning(f"[BOXtilemap] tile present: (layer){layer} (pos){[gx, gy]}")
            return
        
        tile_object = BOXobject(
            size=self.tile_size,
            pos=mul_v2(div2_v2i(pos, self.tile_size), self.tile_size),
            color=[random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
        ); tile_object.tag = tile; tile_object.surface = self.tilesets[tileset][1][tile]

        self.grid.set(tile_object)

        self.surface.blit(tile_object.surface, tile_object.pos)

        self.layers[layer][0][index] = [tile, tileset]
        self.layers[layer][1][index] = tile_object
        BOXlogger.info(f"[BOXtilemap] set tile: (layer){layer} (tile){tile} (tileset){tileset} (pos){mul_v2(div2_v2i(pos, self.tile_size), self.tile_size)}")

    def get_tile(self, layer: str, pos: list[int]) -> BOXobject:
        gx, gy = div2_v2i(pos, self.tile_size)
        if not self.layers.get(layer, False):
            BOXlogger.error(f"[BOXtilemap] failed to get tile: (layer){layer} (pos){[gx, gy]}")
            return
        
        if gx < 0 or gy < 0 or gx >= self.grid_size[0] or gy >= self.grid_size[1]:
            BOXlogger.error(f"[BOXtilemap] failed to get tile: (layer){layer} (pos){[gx, gy]}")
            return

        index = int(gy * self.tile_size[0] + gx)
        if index < 0 or index >= len(self.layers[layer][1]):
            BOXlogger.error(f"[BOXtilemap] failed to get tile: (layer){layer} (pos){[gx, gy]}")
            BOXlogger.error(f"[BOXtilemap] data index out of range: (index){index} (len){len(self.layers[layer][1])}")
            return

        return self.layers[layer][1][index]
    
    def rem_tile(self, layer: str, pos: list[int]) -> None:
        if not self.layers.get(layer, False):
            BOXlogger.error(f"[BOXtilemap] tilemap layer not found: (layer){layer}")
            return
        
        gx, gy = div2_v2i(pos, self.tile_size)
        if gx < 0 or gy < 0 or gx >= self.grid_size[0] or gy >= self.grid_size[1]:
            BOXlogger.error(f"[BOXtilemap] failed to rem tile: (layer){layer} (pos){[gx, gy]}")
            return

        index = int(gy * self.tile_size[0] + gx)
        if index < 0 or index >= len(self.layers[layer][1]):
            BOXlogger.error(f"[BOXtilemap] failed to rem tile: (layer){layer} (pos){[gx, gy]}")
            BOXlogger.error(f"[BOXtilemap] data index out of range: (index){index} (len){len(self.layers[layer][1])}")
            return

        if self.layers[layer][1][index] == None:
            BOXlogger.error(f"[BOXtilemap] tile not present: (layer){layer} (pos){[gx, gy]}")
            return
        
        tile_object = self.layers[layer][1][index]
        self.grid.rem(tile_object)

        self.surface.blit(self._blank, tile_object.pos)
        
        self.layers[layer][0][index] = None
        self.layers[layer][1][index] = None

    def get_tile_region(self, layer:str, size:list[int], pos:list[int]) -> list[BOXobject]:
        if not self.layers.get(layer, False): return
        
        region = self._gen_region(size, pos)
        if not region: return None
        
        tiles = []
        for gx, gy in region:
            index = int(gy * self.tile_size[0] + gx)
            if index < 0 or index >= len(self.layers[layer][1]):
                BOXlogger.error(f"[BOXtilemap] data index out of range: (index){index} (len){len(self.layers[layer][1])}")
                continue
            tile = self.layers[layer][1][index]
            if tile: tiles.append(tile)
        return tiles

    def rem_tile_region(self, layer:str, size:list[int], pos:list[int]) -> None:
        if not self.layers.get(layer, False): return
        
        region = self._gen_region(size, pos)
        if not region: return None
        
        for gx, gy in region:
            index = int(gy * self.tile_size[0] + gx)
            if index < 0 or index >= len(self.layers[layer][1]):
                BOXlogger.error(f"[BOXtilemap] data index out of range: (index){index} (len){len(self.layers[layer][1])}")
                continue
            if self.layers[layer][1][index] == None: continue
            
            self.layers[layer][1][index] = None

        self.grid.rem_region(size, pos)


    """ TILE DATA """
    def import_tileset(self, path: str) -> bool:
        path = rel_path(path)
        if not os.path.exists(path):
            BOXlogger.error(f"[BOXtilemap] failed to import tileset: (path){path}")
            return False
        self.tilesets.append([path, load_surface_array(path, self.tile_size)])
        BOXlogger.info(f"[BOXtilemap] imported tileset: (path){path}")
        return True
    
    def import_data(self, name: str, path: str) -> bool:
        path = rel_path(path)
        if not os.path.exists(path):
            BOXlogger.error(f"[BOXtilemap] failed to import tilemap data: (path){path}")
            return False
        
        path = rel_path(os.path.join(path, f"{name}.json"))
        with open(path, "r") as save:
            data = json.load(save)
            
            config: dict = data["config"]
            layers: dict = data["layers"]

            self._config(self.scene, config["tile_size"], config["grid_size"], config["grid_color"])
            
            tilesets = config["tilesets"]
            for i, tileset in enumerate(tilesets):
                if os.path.exists(tileset):
                    self.tilesets.append([tileset, load_surface_array(tileset, self.tile_size)])
                else:
                    BOXlogger.error(f"[BOXtilemap] tileset not found: {tileset}")
                    return False
            
            for layer in layers:
                for pos, data, in layers[layer].items():
                    if data[0] in (-1, None): continue
                    pos = mul_v2([*map(float, pos.split(","))], self.tile_size)
                    self.set_tile(layer, pos, data[0], data[1])
        
        BOXlogger.info(f"[BOXtilemap] imported tilemap data: (path){path}")
        return True
    
    def export_surface(self, name: str, path: str, grid: bool=False) -> None:
        path = rel_path(path)
        if not os.path.exists(path):
            BOXlogger.error(f"[BOXtilemap] failed to export tilemap image: (name){name} (path){path}")
            return False
        if grid: self._render_grid()
        pg.image.save(self.surface, os.path.join(path, f"{name}.png"))
        BOXlogger.info(f"[BOXtilemap] exported tilemap image: (name){name} (path){path}")

    def export_data(self, name: str, path: str) -> bool:
        path = rel_path(path)
        if not os.path.exists(path):
            BOXlogger.error(f"[BOXtilemap] failed to export tilemap data: (name){name} (path){path}")
            return False

        tilesets = []
        for tileset_path, tiles in self.tilesets:
            tilesets.append(tileset_path)
        
        save_data = {
            "config": {
                "tile_size": self.tile_size,
                "grid_size": self.grid_size,
                "grid_color": self.grid_color,
                "tilesets": tilesets
            },
            "layers": {}
        }

        for layer in self.layers:
            save_data["layers"][layer] = {}
            for tile in self.layers[layer][1]:
                if tile is None: continue
                gx, gy = div2_v2i(tile.pos, self.tile_size)
                index = int(gy * self.tile_size[0] + gx)
                if index < 0 or index >= len(self.layers[layer][1]):
                    BOXlogger.error(f"[BOXtilemap] data index out of range: (index){index} (len){len(self.layers[layer][1])}")
                    continue
                
                save_data["layers"][layer][f"{gx},{gy}"] = self.layers[layer][0][index]
                
        with open(os.path.join(path, f"{name}.json"), "w") as save:
            try:
                json.dump(save_data, save, indent=4, separators=(",", ": "), )
            except json.JSONDecodeError as e: return False
        
        BOXlogger.info(f"[BOXtilemap] exported tilemap data: (name){name} (path){path}")
        return True
    
    def all_data(self, layer:str) -> list[BOXobject]:
        return [data for data in self.layers[layer][0] if data]

    def set_data(self, layer: str, pos: list[int], tile: int, tileset: int) -> None:
        if tile < 0 or tileset < 0 or tileset >= len(self.tilesets): return
        if not self.layers.get(layer, False): return

        gx, gy = div2_v2i(pos, self.tile_size)
        if gx < 0 or gy < 0 or gx >= self.grid_size[0] or gy >= self.grid_size[1]: return

        index = int(gy * self.tile_size[0] + gx)
        if index < 0 or index >= len(self.layers[layer][1]):
            BOXlogger.error(f"[BOXtilemap] data index out of range: (index){index} (len){len(self.layers[layer][1])}")
            return
        if index < 0 or index >= (self.tile_size[0] * self.tile_size[1]): return

        self.layers[layer][0][index] = [tile, tileset]

    def get_data(self, layer: str, pos: list[int]) -> list[int]:
        if not self.layers.get(layer, False): return

        gx, gy = div2_v2i(pos, self.tile_size)
        if gx < 0 or gy < 0 or gx >= self.grid_size[0] or gy >= self.grid_size[1]: return

        index = int(gy * self.tile_size[0] + gx)
        if index < 0 or index >= len(self.layers[layer][1]):
            BOXlogger.error(f"[BOXtilemap] data index out of range: (index){index} (len){len(self.layers[layer][1])}")
            return

        return self.layers[layer][0][index]

    def rem_data(self, layer: str, pos: list[int]) -> None:
        if not self.layers.get(layer, False): return

        gx, gy = div2_v2i(pos, self.tile_size)
        if gx < 0 or gy < 0 or gx >= self.grid_size[0] or gy >= self.grid_size[1]: return

        index = int(gy * self.tile_size[0] + gx)
        if index < 0 or index >= len(self.layers[layer][1]):
            BOXlogger.error(f"[BOXtilemap] data index out of range: (index){index} (len){len(self.layers[layer][1])}")
            return

        self.layers[layer][0][index] = None

    def set_data_region(self, layer:str, size:list[int], pos:list[int], tile: int, tileset: int) -> None:
        if tile < 0 or tileset < 0 or tileset >= len(self.tilesets): return
        if not self.layers.get(layer, False): return
        
        region = self._gen_region(size, pos)
        if not region: return None
        
        for gx, gy in region:
            index = int(gy * self.tile_size[0] + gx)
            if index < 0 or index >= len(self.layers[layer][1]):
                BOXlogger.error(f"[BOXtilemap] data index out of range: (index){index} (len){len(self.layers[layer][1])}")
                continue
            self.layers[layer][0][index] = [tile, tileset]
    
    def get_data_region(self, layer:str, size:list[int], pos:list[int]) -> list[BOXobject]:
        if not self.layers.get(layer, False): return
        
        region = self._gen_region(size, pos)
        if not region: return None
        
        datas = []
        for gx, gy in region:
            index = int(gy * self.tile_size[0] + gx)
            if index < 0 or index >= len(self.layers[layer][1]):
                BOXlogger.error(f"[BOXtilemap] data index out of range: (index){index} (len){len(self.layers[layer][1])}")
                continue
            data = self.layers[layer][0][index]
            if data: datas.append(data)
        return datas

    def rem_data_region(self, layer:str, size:list[int], pos:list[int]) -> None:
        if not self.layers.get(layer, False): return
        
        region = self._gen_region(size, pos)
        if not region: return None
        
        for gx, gy in region:
            index = int(gy * self.tile_size[0] + gx)
            if index < 0 or index >= len(self.layers[layer][1]):
                BOXlogger.error(f"[BOXtilemap] data index out of range: (index){index} (len){len(self.layers[layer][1])}")
                continue
            self.layers[layer][0][index] = None
