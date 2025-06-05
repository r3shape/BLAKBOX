import blakbox

# ------------------------------------------------------------ #
class BOXscene(blakbox.atom.BOXatom):
    def __init__(
            self, app,
            tile_size: list[int] = [32, 32],
            grid_size: list[int] = [50, 50]
        ) -> None:
        super().__init__()
        self.app: blakbox.app.BOXapp = app
        self.cache: blakbox.resource.BOXcache = app.cache
        self.camera: blakbox.pipeline.BOXcamera = blakbox.pipeline.BOXcamera(app.window)
        self.interface: blakbox.pipeline.BOXinterface = blakbox.pipeline.BOXinterface(app.window)
        self.tilemap: blakbox.scene.BOXtilemap = blakbox.scene.BOXtilemap(self, tile_size, grid_size)
        self.renderer: blakbox.pipeline.BOXrenderer = blakbox.pipeline.BOXrenderer(self, app.window, self.camera)
        
    def exit(self) -> None: raise NotImplementedError
    def init(self) -> None: raise NotImplementedError
    def events(self) -> None: raise NotImplementedError
    def update(self, dt: float) -> None: raise NotImplementedError
    def render(self) -> None: raise NotImplementedError
# ------------------------------------------------------------ #