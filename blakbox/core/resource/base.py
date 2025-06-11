from ...globals import pg
from ...log import BOXlogger
from ...atom import BOXprivate, BOXatom

from .game.object import BOXobject

class BOXcache(BOXatom):
    def __init__(self, app):
        super().__init__()
        pg.font.init()
        pg.mixer.init()
        pg.display.init()
        self.app = app
        self.fonts = {}         # key -> (pg.Font, (path, size))
        self.sounds = {}        # key -> (pg.mixer.Sound, path)
        self.objects = {}       # key -> (BOXobject)
        self.surfaces = {}      # key -> (pg.Surface, path)
        self.animations = {}    # key -> (list[pg.Surface], list[index, timer, duration, loop])

    @BOXprivate
    def _load_surface(self, path: str) -> pg.Surface:
        try:
            return pg.image.load(path).convert_alpha()
        except Exception as e:
            BOXlogger.error(f"[BOXcache] Failed to load surface '{path}': {e}")
            return None

    @BOXprivate
    def _load_surface_array(self, path: str, frame_size: list[int]) -> list[pg.Surface]:
        sheet = self._load_surface(path)
        frame_x = sheet.get_width() // frame_size[0]
        frame_y = sheet.get_height() // frame_size[1]

        frames = []
        for row in range(frame_y):
            for col in range(frame_x):
                x = col * frame_size[0]
                y = row * frame_size[1]
                frame = pg.Surface(frame_size, pg.SRCALPHA).convert_alpha()
                frame.blit(sheet, [0, 0], pg.Rect([x, y], frame_size))  # texture sampling :)
                frames.append(frame)
        return frames

    @BOXprivate
    def _load_font(self, path: str, size: int) -> pg.font.Font:
        try:
            return pg.font.Font(path, size)
        except Exception as e:
            BOXlogger.error(f"[BOXcache] Failed to load font '{path}' size {size}: {e}")
            return None

    @BOXprivate
    def _load_sound(self, path: str) -> pg.mixer.Sound:
        try:
            return pg.mixer.Sound(path)
        except Exception as e:
            BOXlogger.error(f"[BOXcache] Failed to load sound '{path}': {e}")
            return None

    def load_surface(self, key: str, path: str) -> bool:
        if key in self.surfaces:
            BOXlogger.warning(f"[BOXcache] Surface already exists: '{key}'. Use reload_surface() to overwrite.")
            return False
        surface = self._load_surface(path)
        if surface:
            self.surfaces[key] = (surface, path)
            BOXlogger.info(f"[BOXcache] Surface loaded: (key){key} (path){path}")
            return True
        return False

    def reload_surface(self, key: str, path: str) -> bool:
        if key not in self.surfaces:
            BOXlogger.warning(f"[BOXcache] Surface not found: {key}")
            return False
        
        surface = self._load_surface(path)
        if surface:
            self.surfaces[key] = (surface, path)
            BOXlogger.info(f"[BOXcache] Reloaded surface with key: '{key}'")
            return True
        return False

    def get_surface(self, key: str) -> pg.Surface | None:
        return self.surfaces.get(key, (None,))[0]

    def unload_surface(self, key: str) -> None:
        if key not in self.surfaces:
            BOXlogger.warning(f"[BOXcache] Surface not found: {key}")
            return
        del self.surfaces[key]
        BOXlogger.info(f"[BOXcache] Unloaded surface with key: '{key}'")

    def load_animation(self, key: str, path: str, frame_size: list[int], frame_duration: float, loop: bool = True) -> None:
        if key in self.surfaces:
            BOXlogger.warning(f"[BOXcache] Animation already exists: '{key}'. Use reload_animation() to overwrite.")
            return False
        
        frames = self._load_surface_array(path, frame_size)
        if frames:
            self.animations[key] = [frames, [0, 0.0, len(frames), 1/frame_duration, loop]]
            BOXlogger.info(f"[BOXcache] Animation loaded: (key){key} (path){path}")
            return True
        return False
    
    def reload_animation(self, key: str, path: str, frame_size: list[int], frame_duration: float, loop: bool = True) -> bool:
        if key not in self.animations:
            BOXlogger.warning(f"[BOXcache] Animation not found: {key}")
            return False
        
        frames = self._load_surface_array(path, frame_size)
        if frames:
            self.animations[key] = [frames, [0, 0.0, len(frames), 1/frame_duration, loop]]
            BOXlogger.info(f"[BOXcache] Reloaded animation with key: '{key}'")
            return True
        return False

    def get_animation(self, key: str) -> list:
        return self.animations.get(key, None)

    def get_animation_frames(self, key: str) -> list:
        return self.animations.get(key, None)[0]

    def get_animation_data(self, key: str) -> list:
        return self.animations.get(key, None)[1]
    
    def get_animation_frame(self, key: str) -> list:
        data = self.get_animation(key)
        if not data:
            BOXlogger.warning(f"[BOXcache] Animation not found: '{key}'")
            return
        return data[0][data[1][0]]
    
    def reset_animation(self, key: str) -> None:
        data = self.get_animation(key)
        if not data:
            BOXlogger.warning(f"[BOXcache] Animation not found: '{key}'")
            return
        data[1][1] = 0
        data[1][0] = 0

    def update_animation(self, key: str, dt: float) -> None:
        data = self.get_animation(key)
        if not data:
            BOXlogger.warning(f"[BOXcache] Animation not found: '{key}'")
            return

        data[1][1] += dt
        if data[1][1] >= data[1][3]:
            data[1][1] = 0
            data[1][0] += 1
            if data[1][0] >= data[1][2]:
                if data[1][4]:
                    data[1][0] = 0
                else:
                    data[1][0] = data[1][2] - 1

    def unload_animation(self, key: str) -> None:
        if key not in self.animations:
            BOXlogger.warning(f"[BOXcache] Animation not found: {key}")
            return
        del self.animations[key]
        BOXlogger.info(f"[BOXcache] Unloaded animation with key: '{key}'")

    def load_font(self, key: str, path: str, size: int) -> bool:
        if key in self.fonts:
            BOXlogger.warning(f"[BOXcache] Font already exists: '{key}'. Use reload_font() to overwrite.")
            return False
        font = self._load_font(path, size)
        if font:
            self.fonts[key] = (font, (path, size))
            BOXlogger.info(f"[BOXcache] Font loaded: (key){key} (path){path}")
            return True
        return False

    def reload_font(self, key: str, path: str, size: int) -> bool:
        if key not in self.fonts:
            BOXlogger.warning(f"[BOXcache] Font not found: {key}")
            return False

        font = self._load_font(path, size)
        if font:
            self.fonts[key] = (font, (path, size))
            BOXlogger.info(f"[BOXcache] Reloaded font with key: '{key}'")
            return True
        return False

    def get_font(self, key: str) -> pg.font.Font | None:
        return self.fonts.get(key, (None,))[0]

    def unload_font(self, key: str) -> None:
        if key not in self.fonts:
            BOXlogger.warning(f"[BOXcache] Font not found: {key}")
            return
        del self.fonts[key]
        BOXlogger.info(f"[BOXcache] Unloaded font with key: '{key}'")

    def load_sound(self, key: str, path: str) -> bool:
        if key in self.sounds:
            BOXlogger.warning(f"[BOXcache] Sound already exists: '{key}'. Use reload_sound() to overwrite.")
            return False
        sound = self._load_sound(path)
        if sound:
            self.sounds[key] = (sound, path)
            BOXlogger.info(f"[BOXcache] Sound loaded: (key){key} (path){path}")
            return True
        return False

    def reload_sound(self, key: str, path: str) -> bool:
        if key not in self.sounds:
            BOXlogger.warning(f"[BOXcache] Sound not found: {key}")
            return False
        
        sound = self._load_sound(path)
        if sound:
            self.sounds[key] = (sound, path)
            BOXlogger.info(f"[BOXcache] Reloaded sound with key: '{key}'")
            return True
        return False

    def get_sound(self, key: str) -> pg.mixer.Sound | None:
        return self.sounds.get(key, (None,))[0]

    def unload_sound(self, key: str) -> None:
        if key not in self.sounds:
            BOXlogger.warning(f"[BOXcache] Sound not found: {key}")
            return
        del self.sounds[key]
        BOXlogger.info(f"[BOXcache] Unloaded sound with key: '{key}'")

    def load_object(
            self,
            key: str,
            mass: float = 10.0,
            speed: float = 100.0,
            size: list[int] = [8, 8],
            pos: list[float] = [0, 0],
            bounds: list[int] = [0, 0],
            color: list[int] = [0, 0, 0],
            flags: int = 0,
        ) -> BOXobject:
            if self.app.scene is None:
                BOXlogger.error(f"[BOXcache] Scene not set: '{key}'. A call to both add_scene() and set_scene() must be made first.")
                return None

            if key in self.objects:
                BOXlogger.warning(f"[BOXcache] Object already exists: '{key}'. Use reload_object() to overwrite.")
                return self.objects[key]
            
            self.objects[key] = BOXobject(
                tag=key,
                pos=pos,
                size=size,
                mass=mass,
                speed=speed,
                color=color,
                bounds=bounds,
                flags = flags
            )
            self.app.scene.tilemap.grid.set(self.objects[key])
            
            BOXlogger.info(f"[BOXcache] Object loaded: (key){key} (path){size} (pos){pos}")
            return self.objects[key]

    def get_object(self, key: str) -> pg.mixer.Sound | None:
        return self.objects.get(key, None)

    def reload_object(
            self,
            key: str,
            mass: float = 10.0,
            speed: float = 100.0,
            size: list[int] = [8, 8],
            pos: list[float] = [0, 0],
            bounds: list[int] = [0, 0],
            color: list[int] = [0, 0, 0],
            flags: int = 0,
        ) -> BOXobject:
        if key not in self.objects:
            BOXlogger.warning(f"[BOXcache] Object not found: {key}")
            return None

        self.objects[key] = self.load_object(key, mass, speed, size, pos, bounds, color, flags)
        
        BOXlogger.info(f"[BOXcache] Reloaded object with key: '{key}'")
        return self.objects[key]
    
    def unload_object(self, key: str) -> None:
        if key not in self.objects:
            BOXlogger.warning(f"[BOXcache] Object not found: {key}")
            return
        del self.objects[key]
        BOXlogger.info(f"[BOXcache] Unloaded object with key: '{key}'")

    def clear(self) -> None:
        self.fonts.clear()
        self.sounds.clear()
        self.objects.clear()
        self.surfaces.clear()
        self.animations.clear()
        BOXlogger.info("[BOXcache] Cleared all cached assets")
