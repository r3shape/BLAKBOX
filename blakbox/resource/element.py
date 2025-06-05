from ..globals import pg, Optional
from ..log import BOXlogger
from ..app.inputs import BOXmouse
from ..app.events import BOXevents
from ..app.window import BOXwindow
from ..atom import BOXprivate, BOXatom
from ..utils import add_v2, sub_v2, div_v2, point_inside

class BOXelement(BOXatom):
    class flags:
        # Visibility flags
        VISIBLE: int                 = 1 << 0
        SHOW_TEXT: int               = 1 << 2
        SHOW_BORDER: int             = 1 << 3
        SHOW_SURFACE: int            = 1 << 4
        SHOW_ELEMENTS: int           = 1 << 5

        # Alignment flags
        ALIGN_LEFT: int              = 1 << 6
        ALIGN_RIGHT: int             = 1 << 7
        ALIGN_CENTER: int            = 1 << 8

        # Anchor flags
        ANCHOR_CENTER: int           = 1 << 9
        ANCHOR_TOP_LEFT: int         = 1 << 10
        ANCHOR_TOP_RIGHT: int        = 1 << 11
        ANCHOR_TOP_CENTER: int       = 1 << 12
        ANCHOR_BOTTOM_LEFT: int      = 1 << 13
        ANCHOR_BOTTOM_RIGHT: int     = 1 << 14
        ANCHOR_BOTTOM_CENTER: int    = 1 << 15

        # Interaction flags
        HOVERED: int                 = 1 << 16
        CLICKED: int                 = 1 << 17
        
        # Visual Flags
        ANTI_ALIAS: int              = 1 << 18
        DISPLAY_ROW: int             = 1 << 19
        DISPLAY_LIST: int            = 1 << 20

    def __init__(
            self,
            pos: list[float] = [0, 0],
            size: list[int] = [10, 10],
            color: list[int] = [255, 255, 255],
            border_width: int = 1,
            border_color: list[int] = [0, 0, 0],
            border_radius: list[int] = [0, 0, 0, 0],
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

        self.set_flag(BOXelement.flags.VISIBLE)
        self.set_flag(BOXelement.flags.SHOW_BORDER)
        self.set_flag(BOXelement.flags.SHOW_SURFACE)
        self.set_flag(BOXelement.flags.SHOW_ELEMENTS)

    def on_click(self) -> None: pass
    def on_hover(self) -> None: pass
    def on_unhover(self) -> None: pass
    def on_render(self, surface: pg.Surface) -> None: pass
    def on_update(self, events: BOXevents) -> None: pass

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
        BOXlogger.info(f"[BOXinterface] Set element: (key){key}")
    
    def get_element(self, key: str) -> "BOXelement":
        return self.children.get(key, None)
    
    def rem_element(self, key: str) -> None:
        if key not in self.children: return
        self.children[key].parent = None
        del self.children[key]
        BOXlogger.info(f"[BOXinterface] Removed element: (key){key}")

    def clear(self) -> None:
        for element in self.children.values():
            element.parent = None
            element.clear()
        self.children.clear()
        BOXlogger.info("[BOXinterface] Cleared all elements")

    def _render(self, surface: pg.Surface) -> None:
        if not self.get_flag(BOXelement.flags.VISIBLE):
            return

        if self.get_flag(BOXelement.flags.SHOW_SURFACE):
            self.surface.fill(self.color)
            self.on_render(self.surface)
            surface.blit(self.surface, self.absolute_pos)

            if self.get_flag(BOXelement.flags.SHOW_ELEMENTS):
                for child in self.children.values():
                    child._render(surface)
        else:
            self.on_render(surface)
            if self.get_flag(BOXelement.flags.SHOW_ELEMENTS):
                for child in self.children.values():
                    child._render(surface)

        if self.get_flag(BOXelement.flags.SHOW_BORDER):
            pg.draw.rect(
                surface=surface,
                rect=self.absolute_rect,
                color=self.border_color,
                width=self.border_width,
                border_top_left_radius=self.border_radius[0],
                border_top_right_radius=self.border_radius[1],
                border_bottom_left_radius=self.border_radius[2],
                border_bottom_right_radius=self.border_radius[3]
            )

# def get_position(self, screen_size: list[int]) -> list[int]:
#     x, y = self.pos
#     w, h = self.size
#     sw, sh = screen_size
#     ox, oy = self.offset

#     if self.get_flag(self.flags.ANCHOR_TOP_LEFT):
#         x, y = ox, oy
#     elif self.get_flag(self.flags.ANCHOR_TOP_CENTER):
#         x, y = sw // 2 - w // 2 - ox, oy
#     elif self.get_flag(self.flags.ANCHOR_TOP_RIGHT):
#         x, y = sw - w - ox, oy
#     elif self.get_flag(self.flags.ANCHOR_CENTER):
#         x, y = sw // 2 - w // 2 - ox, sh // 2 - h // 2 - oy
#     elif self.get_flag(self.flags.ANCHOR_BOTTOM_LEFT):
#         x, y = ox, sh - h - oy
#     elif self.get_flag(self.flags.ANCHOR_BOTTOM_CENTER):
#         x, y = sw // 2 - w // 2 - ox, sh - h - oy
#     elif self.get_flag(self.flags.ANCHOR_BOTTOM_RIGHT):
#         x, y = sw - w - ox, sh - h - oy

#     if self.font:
#         tw, th = self.font.size(self.text)
#         if self.get_flag(self.flags.ALIGN_LEFT):
#             x += tw
#         elif self.get_flag(self.flags.ALIGN_RIGHT):
#             x -= tw
#         elif self.get_flag(self.flags.ALIGN_CENTER):
#             x -= tw // 2
#             y -= th // 2

#     return [x, y]