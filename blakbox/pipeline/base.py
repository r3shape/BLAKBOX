from blakbox.atom import BOXatom

class BOXpipelineFlag(BOXatom):
    __slots__ = (
        "BOUNDED",
        "SCREEN_CLIP",
        "VIEW_CLIP",
    )

    def __init__(self):
        super().__init__()
        self._unfreeze()
        self.BOUNDED: int = (1 << 0)
        self.SCREEN_CLIP: int = (1 << 1)
        self.VIEW_CLIP: int = (1 << 2)
        self._freeze()
        
BOXpipelineFlag = BOXpipelineFlag()
