from blakbox.atom import BOXprivate, BOXatom
from blakbox.utils import mul_v2
from blakbox.log import BOXlogger
from blakbox.globals import os, pg

from collections import namedtuple

BOXhandle = namedtuple("BOXhandle", ["resource", "index"])
BOXresourceData = namedtuple("BOXresourceData", ["surface", "surfarray", "object"])

class BOXresource(BOXatom):
    __slots__ = (
        "_resource",
        "_atlas",
        "_atlas_pos",
        "_resource_max",
        "_atlas_size",
    )

    def __init__(
            self,
            atlas_size: list[int] = [1280, 720]
    ) -> None:
        super().__init__()

        self._unfreeze()
        self._resource_max: int = 4069
        self._resource: BOXresourceData = BOXresourceData(surface = [], surfarray=[], object = [])
        
        self._atlas_pos: list[int] = [0, 0]
        self._atlas_size: list[int] = atlas_size[:]
        self._atlas: pg.Surface = pg.Surface(atlas_size, pg.SRCALPHA)
        self._atlas.set_colorkey([1, 2, 3])
        self._atlas.fill([1, 2, 3])
        self._freeze()
        
    def _load_surface(self, filepath: str, scale: list[int] = None, color_key: list[int] = None) -> pg.Surface:
        surface = pg.image.load(filepath).convert_alpha()
        if scale:
            surface = pg.transform.scale(surface, scale)
        if color_key:
            surface.set_colorkey(color_key)
        return surface

    def _load_surfacev(self, filepath: str, size: list[int], scale: list[int] = None, color_key: list[int] = None) -> list[pg.Surface]:
        sheet: pg.Surface = pg.image.load(filepath)
        
        frames = []
        frame_x = sheet.get_width() // size[0]
        frame_y = sheet.get_height() // size[1]

        for row in range(frame_y):
            for col in range(frame_x):
                x = col * size[0]
                y = row * size[1]
                frame = pg.Surface(size, pg.SRCALPHA).convert_alpha()
                if color_key:
                    frame.set_colorkey(color_key)
                frame.blit(sheet, (0, 0), pg.Rect((x, y), size))
                if scale:
                    frame = self.scale_surface(frame, scale)
                frames.append(frame)
        return frames

    def _surface_test(self, surface: pg.Surface, threshold: int = 1) -> bool:
        pixels, transparent = 0, 0
        for y in range(surface.get_height()):
            for x in range(surface.get_width()):
                if surface.get_at((x, y)).a == 0:
                    transparent += 1
                pixels += 1
        return (pixels - transparent) >= threshold

    def _handle_valid(self, handle: BOXhandle) -> bool:
        if not isinstance(handle, BOXhandle): return False
        
        resource, index = handle
        if resource < 0 or index < 0: return False
        if resource >= len(self._resource) or index > len(self._resource[resource]): return False

        return True

    def get(self, handle: BOXhandle):
        if not self._handle_valid(handle): return [None, None]

        resource, index = handle
        match resource:
            case 0: return self._resource[resource][index]
            case 1: return self._resource[resource][index]
            case 2: return self._resource[resource][index]
            case _: return [None, None]

    def rem(self, handle: BOXhandle):
        if not self._handle_valid(handle): return

        resource, index = handle
        match resource:
            case 0:
                data = self._resource[resource][index]
                
                pos = data[1]
                size = data[2]
                surf = pg.Surface(size, pg.SRCALPHA)
                rect = surf.fill([1, 2, 3])
                self._atlas.blit(surf, pos, rect)
                
                del surf
                del rect

                filepath = data[0]
                BOXlogger.info(f"[BOXresource] removed surface: (pos){pos} (size){size} (filepath){filepath}")
            case 1:
                data = self._resource[resource][index]
                
                pos = data[1]
                size = data[2]
                layout = data[3]
                speed = data[5]
                surf = pg.Surface(size, pg.SRCALPHA)
                rect = surf.fill([1, 2, 3])
                self._atlas.blit(surf, pos, rect)
                
                del surf
                del rect

                filepath = data[0]
                BOXlogger.info(f"[BOXresource] removed surfarray: (speed){speed} (pos){pos} (size){size} (layout){layout} (filepath){filepath}")                
            case 2:
                data = self._resource[resource][index]
                pos = data[0]
                size = data[2]
                speed = data[3]
                BOXlogger.info(f"[BOXresource] removed object: (pos){pos} (size){size} (speed){speed}")
            case _: return
        
        self._resource[resource][index] = None

    @BOXprivate
    def load_surface(
            self,
            filepath: str,
            size: list[int],
            scale: list[int] = None,
            layout: list[int] = [1, 1],
            color: list[int] = [0, 0, 0],
            color_key: list[int] = None
            ) -> BOXhandle:
        if not os.path.exists(filepath):
            BOXlogger.error(f"[BOXresource] filepath not found: {filepath}")
            return BOXhandle(-1, -1)
        
        resource = 0
        index = len(self._resource[resource])
        if index >= self._resource_max:
            BOXlogger.warning(f"[BOXresource] resource max reached")
            return BOXhandle(-1, -1)

        surf = self._load_surface(filepath, scale, color_key)

        x, y = self._atlas_pos
        w, h = mul_v2(size, layout[:])
        if x + w >= self._atlas_size[0]:
            self._atlas_pos[0] = 0
            if y + h + self._resource[resource][index - 1][1][1] > self._atlas_size[1]:
                BOXlogger.error(f"[BOXresource] atlas too small")
                return BOXhandle(-1, -1)
            for pos, size in self._resource[resource]:
                if h < size[1]:
                    h = size[1]
            self._atlas_pos[1] += h

        data = [filepath, self._atlas_pos[:], size[:], layout[:], pg.Rect(self._atlas_pos, size), scale, color, color_key]
        self._atlas.blit(surf, self._atlas_pos)
        self._atlas_pos[0] += w

        self._resource[resource].append(data)
        del surf

        BOXlogger.info(f"[BOXresource] loaded surface: (pos){data[1]} (size){data[2]} (filepath){filepath}")
        return BOXhandle(resource, index)

    @BOXprivate
    def load_surfarray(
            self,
            filepath: str,
            size: list[int],
            layout: list[int],
            speed: float=5.0,
            scale: list[int] = None,
            color: list[int] = [0, 0, 0],
            color_key: list[int] = None,
    ) -> None:
        surf_handle = self.load_surface(filepath, size, scale, layout, color, color_key)
        if not self._handle_valid(surf_handle):
            BOXlogger.warning(f"[BOXresource] failed to load surfarray surface: (filepath){filepath}")
            return BOXhandle(-1, -1)

        resource = 1
        index = len(self._resource[resource])
        if index >= self._resource_max:
            BOXlogger.warning(f"[BOXresource] resource max reached")
            return BOXhandle(-1, -1)

        filepath, pos, size, layout, rect, scale, color, color_key = self.get(surf_handle)
        data = [filepath, pos, size, rect, layout, speed, scale, color, color_key]

        self._resource[resource].append(data)
        
        BOXlogger.info(f"[BOXresource] loaded surfarray: (speed){speed} (pos){pos} (size){size} (layout){layout} (filepath){filepath}")
        return BOXhandle(resource, index)

    @BOXprivate
    def load_object(
            self,
            pos: list[int],
            size: list[int],
            speed: float = 100.0
            ) -> BOXhandle:
        resource = 2
        index = len(self._resource[resource])
        if index >= self._resource_max:
            BOXlogger.warning(f"[BOXresource] resource max reached")
            return BOXhandle(-1, -1)

        data = [pos[:], [0, 0, 0, 0], size[:], speed]
        self._resource[resource].append(data)

        BOXlogger.info(f"[BOXresource] loaded object: (pos){pos} (size){size} (speed){speed}")
        return BOXhandle(resource, index)
