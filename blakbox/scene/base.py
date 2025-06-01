from blakbox.atom import BOXatom

import blakbox

class BOXscene(BOXatom):
    __slots__ = (
        "_app",
        "_grid",
        "_resource",
        "_world",
        "_camera",
        "_physics",
        "_renderer",
        "_interface"
    )

    def __init__(
            self, app,
            cell_size: int,
            cell_count: list[int]
    ) -> None:
        super().__init__()

        self._unfreeze()
        self._app: blakbox.app.base.BOXapplication = app
        self._resource: blakbox.resource.base.BOXresource = app._resource

        self._physics: blakbox.pipeline.physics.BOXphysics = blakbox.pipeline.physics.BOXphysics(self)
        self._grid: blakbox.scene.grid.BOXgrid = blakbox.scene.grid.BOXgrid(cell_size, cell_count)
        
        self._camera: blakbox.pipeline.camera.BOXcamera = blakbox.pipeline.camera.BOXcamera(self, [0, 0], self._grid.size)
        self._interface: blakbox.pipeline.interface.BOXinterface = blakbox.pipeline.interface.BOXinterface(self)
        self._renderer: blakbox.pipeline.render.BOXrenderer = blakbox.pipeline.render.BOXrenderer(self)
        self._world: blakbox.pipeline.world.BOXworld = blakbox.pipeline.world.BOXworld(self)
        self._freeze()
        
    @property
    def app(self):
        return self._app

    @property
    def grid(self):
        return self._grid
    
    @property
    def resource(self):
        return self._app.resource

    @property
    def camera(self):
        return self._camera

    @property
    def renderer(self):
        return self._renderer
    
    def on_init(self) -> None:
        raise NotImplementedError
    
    def on_exit(self) -> None:
        raise NotImplementedError
    
    def on_event(self) -> None:
        raise NotImplementedError
    
    def on_update(self) -> None:
        raise NotImplementedError

