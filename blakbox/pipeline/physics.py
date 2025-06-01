from blakbox.atom import BOXatom

import blakbox

class BOXphysics(BOXatom):
    __slots__ = (
        "_scene",
        "_resource",
    )
    
    def __init__(
            self,
            scene: blakbox.scene.base.BOXscene
    ) -> None:
        super().__init__()

        self._unfreeze()
        self._scene: blakbox.scene.base.BOXscene = scene
        self._resource: blakbox.resource.base.BOXresource = scene._resource
        self._freeze()
        
    @property
    def scene(self):
        return self._scene
    
    def update(self, dt: float) -> None: pass

