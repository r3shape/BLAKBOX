from ....globals import pg, Optional
from ....log import BOXlogger
from ...app.inputs import BOXmouse
from ...app.events import BOXevents
from ...app.window import BOXwindow
from ....atom import BOXprivate, BOXatom
from ....utils import add_v2, sub_v2, div_v2, point_inside

class BOXelement(BOXatom):
    class flags:
        # Visibility flags
        VISIBLE: int                 = 1 << 0
        SHOW_TEXT: int               = 1 << 2
        SHOW_BORDER: int             = 1 << 3
        SHOW_ELEMENTS: int           = 1 << 4

        # Anchor flags
        ANCHOR_CENTER: int           = 1 << 5
        ANCHOR_TOP_LEFT: int         = 1 << 6
        ANCHOR_TOP_RIGHT: int        = 1 << 7
        ANCHOR_TOP_CENTER: int       = 1 << 8
        ANCHOR_BOTTOM_LEFT: int      = 1 << 9
        ANCHOR_BOTTOM_RIGHT: int     = 1 << 10
        ANCHOR_BOTTOM_CENTER: int    = 1 << 11

        # Interaction flags
        HOVERED: int                 = 1 << 12
        CLICKED: int                 = 1 << 13
        
        # Visual Flags
        ANTI_ALIAS: int              = 1 << 14

    def __init__(
            self,
            pos: list[float] = [0, 0],
            size: list[int] = [10, 10],
            color: list[int] = [255, 255, 255],
            border_width: int = 1,
            border_color: list[int] = [0, 0, 0],
            border_radius: list[int] = [0, 0, 0, 0],
            flags: int = 0,
    ) -> None:
        super().__init__()
        self.size: list[int] = size[:]
        self.pos: list[float] = pos[:]
        self.color: list[int] = color[:]
        
        self.border_width: int = border_width
        self.border_color: list[int] = border_color[:]
        self.border_radius: list[int] = border_radius[:]

        self.parent: Optional[BOXelement] = None
        self.children: dict[str, BOXelement] = {}

        self.surface: pg.Surface = pg.Surface(size, pg.SRCALPHA)
        self.surface.fill(color)

        self.set_flag(flags)
        self.set_flag(BOXelement.flags.VISIBLE)
        self.set_flag(BOXelement.flags.ANTI_ALIAS)
        self.set_flag(BOXelement.flags.SHOW_BORDER)
        self.set_flag(BOXelement.flags.SHOW_ELEMENTS)

    def on_click(self) -> None: pass
    def on_hover(self) -> None: pass
    def on_unhover(self) -> None: pass
    def on_update(self, events: BOXevents) -> None: pass
    def on_render(self, surface: pg.Surface) -> None: pass

    @property
    def rect(self) -> pg.Rect:
        return pg.Rect(self.pos, self.size)

    @property
    def absolute_pos(self) -> list[float]:
        if self.parent:
            return add_v2(self.pos, self.parent.absolute_pos)
        return self.pos[:]

    @property
    def absolute_rect(self) -> pg.Rect:
        return pg.Rect(self.absolute_pos, self.size)

    def set_element(self, key: str, element: "BOXelement") -> None:
        if key in self.children: return
        element.parent = self
        self.children[key] = element
        BOXlogger.info(f"[BOXelement] Set child element: (key){key}")
    
    def get_element(self, key: str) -> "BOXelement":
        return self.children.get(key, None)
    
    def rem_element(self, key: str) -> None:
        if key not in self.children: return
        self.children[key].parent = None
        del self.children[key]
        BOXlogger.info(f"[BOXelement] Removed child element: (key){key}")

    def clear(self) -> None:
        for element in self.children.values():
            element.parent = None
            element.clear()
        self.children.clear()
        BOXlogger.info("[BOXelement] Cleared all child elements")

    @BOXprivate
    def _update_hook(self, events: BOXevents) -> None: pass
    
    @BOXprivate
    def _render_hook(self, target: pg.Surface) -> None: pass

    def _render(self, target: pg.Surface) -> None:
        if not self.get_flag(BOXelement.flags.VISIBLE):
            return

        self.surface.fill(self.color)
        if self.get_flag(BOXelement.flags.SHOW_ELEMENTS):
            for child in self.children.values():
                child._render(self.surface)
        
        self.on_render(self.surface)        # user render hook
        self._render_hook(self.surface)     # internal render hook
        target.blit(self.surface, self.pos)

        if self.get_flag(BOXelement.flags.SHOW_BORDER):
            pg.draw.rect(
                surface=target,
                rect=self.rect,
                color=self.border_color,
                width=self.border_width,
                border_top_left_radius=self.border_radius[0],
                border_top_right_radius=self.border_radius[1],
                border_bottom_left_radius=self.border_radius[2],
                border_bottom_right_radius=self.border_radius[3]
            )
