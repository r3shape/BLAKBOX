from ..globals import pg
from ..log import BOXlogger
from ..atom import BOXprivate, BOXatom

class BOXcache(BOXatom):
    def __init__(self):
        super().__init__()
        pg.font.init()
        pg.mixer.init()
        pg.display.init()
        self.fonts = {}    # key -> (pg.Font, (path, size))
        self.sounds = {}   # key -> (pg.mixer.Sound, path)
        self.surfaces = {} # key -> (pg.Surface, path)

    @BOXprivate
    def _load_surface(self, path: str) -> pg.Surface:
        try:
            return pg.image.load(path).convert_alpha()
        except Exception as e:
            BOXlogger.error(f"[BOXcache] Failed to load surface '{path}': {e}")
            return None

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
            BOXlogger.warning(f"[BOXcache] Surface key '{key}' already exists. Use reload_surface() to overwrite.")
            return False
        surface = self._load_surface(path)
        if surface:
            self.surfaces[key] = (surface, path)
            BOXlogger.info(f"[BOXcache] Surface loaded: (key){key} (path){path}")
            return True
        return False

    def reload_surface(self, key: str, path: str) -> bool:
        surface = self._load_surface(path)
        if surface:
            self.surfaces[key] = (surface, path)
            BOXlogger.info(f"[BOXcache] Reloaded surface with key '{key}'")
            return True
        return False

    def get_surface(self, key: str) -> pg.Surface | None:
        return self.surfaces.get(key, (None,))[0]

    def unload_surface(self, key: str) -> None:
        if key in self.surfaces:
            del self.surfaces[key]
            BOXlogger.info(f"[BOXcache] Unloaded surface with key '{key}'")

    def load_font(self, key: str, path: str, size: int) -> bool:
        if key in self.fonts:
            BOXlogger.warning(f"[BOXcache] Font key '{key}' already exists. Use reload_font() to overwrite.")
            return False
        font = self._load_font(path, size)
        if font:
            self.fonts[key] = (font, (path, size))
            BOXlogger.info(f"[BOXcache] Font loaded: (key){key} (path){path}")
            return True
        return False

    def reload_font(self, key: str, path: str, size: int) -> bool:
        font = self._load_font(path, size)
        if font:
            self.fonts[key] = (font, (path, size))
            BOXlogger.info(f"[BOXcache] Reloaded font with key '{key}'")
            return True
        return False

    def get_font(self, key: str) -> pg.font.Font | None:
        return self.fonts.get(key, (None,))[0]

    def unload_font(self, key: str) -> None:
        if key in self.fonts:
            del self.fonts[key]
            BOXlogger.info(f"[BOXcache] Unloaded font with key '{key}'")

    def load_sound(self, key: str, path: str) -> bool:
        if key in self.sounds:
            BOXlogger.warning(f"[BOXcache] Sound key '{key}' already exists. Use reload_sound() to overwrite.")
            return False
        sound = self._load_sound(path)
        if sound:
            self.sounds[key] = (sound, path)
            BOXlogger.info(f"[BOXcache] Sound loaded: (key){key} (path){path}")
            return True
        return False

    def reload_sound(self, key: str, path: str) -> bool:
        sound = self._load_sound(path)
        if sound:
            self.sounds[key] = (sound, path)
            BOXlogger.info(f"[BOXcache] Reloaded sound with key '{key}'")
            return True
        return False

    def get_sound(self, key: str) -> pg.mixer.Sound | None:
        return self.sounds.get(key, (None,))[0]

    def unload_sound(self, key: str) -> None:
        if key in self.sounds:
            del self.sounds[key]
            BOXlogger.info(f"[BOXcache] Unloaded sound with key '{key}'")

    def clear(self) -> None:
        self.fonts.clear()
        self.sounds.clear()
        self.surfaces.clear()
        BOXlogger.info("[BOXcache] Cleared all cached assets")
