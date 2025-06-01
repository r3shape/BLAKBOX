from blakbox.atom import BOXatom

import blakbox

class BOXworld(BOXatom):
    __slots__ = (
        "_scene",
        "_resource",
        "_window",
        "_camera"
    )

    def __init__(
            self,
            scene: blakbox.scene.base.BOXscene
    ) -> None:
        super().__init__()

        self._unfreeze()
        self._scene: blakbox.scene.base.BOXscene = scene
        self._resource: blakbox.resource.base.BOXresource = scene._resource
        self._window: blakbox.app.window.BOXwindow = scene.app.window
        self._camera: blakbox.pipeline.camera.BOXcamera = scene._camera
        self._freeze()
        
    @property
    def scene(self):
        return self._scene

    def update(self) -> None: pass

