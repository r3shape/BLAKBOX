from ..globals import pg
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
        DISPLAY_LIST: int            = 1 << 19

    def __init__(
            self,
            text: str = None,
            font: pg.Font = None,
            pos: list[float] = [0, 0],
            padding: list[int] = [0, 0],
            size: list[int] = [100, 100],
            offset: list[float] = [0, 0],
            color: list[int] = [155, 155, 155],
            text_color: list[int] = [0, 0, 0],
            text_offset: list[float] = [0, 0],
            border_width: int = 1,
            border_size: list[int] = [1, 1],
            border_color: list[int] = [255, 0, 0],
            border_radius: list[int] = [0, 0, 0, 0],
        ) -> None:
        super().__init__()
        self.text: str = text
        self.font: pg.Font = font
        self.pos: list[float] = pos[:]
        self.size: list[int] = size[:]
        self.color: list[int] = color[:]
        self.padding: list[int] = padding[:]
        self.offset: list[float] = offset[:]
        self.text_color: list[int] = text_color[:]
        self.text_pos: list[float] = text_offset[:]
        
        self.border_width: int = border_width
        self.border_color: list[int] = border_color[:]
        self.border_radius: list[int] = border_radius[:]

        self.surface: pg.Surface = pg.Surface(size, pg.SRCALPHA)
        self.surface.fill(color)

        self.elements: dict[str, BOXelement] = {}

        self.set_flag(self.flags.VISIBLE)
        self.set_flag(self.flags.SHOW_TEXT)
        self.set_flag(self.flags.ANTI_ALIAS)
        self.set_flag(self.flags.SHOW_SURFACE)

    @property
    def rect(self) -> pg.Rect:
        return pg.Rect(self.pos, self.size)

    def set_element(self, key: str, element: "BOXelement") -> None:
        if self.get_element(key): return
        element.pos = add_v2(element.pos, self.pos)
        self.elements[key] = element
    
    def get_element(self, key: str) -> "BOXelement":
        return self.elements.get(key, None)
    
    def rem_element(self, key: str) -> None:
        if self.get_element(key) is not None:
            elem = self.elements.pop(key)
            del elem

    def on_click(self) -> None: BOXlogger.info("[BOXelement] on click!")
    def on_hover(self) -> None: BOXlogger.info("[BOXelement] on hover!")
    def on_unhover(self) -> None: BOXlogger.info("[BOXelement] on unhover!")

    def get_position(self, screen_size: list[int]) -> list[int]:
        x, y = self.pos
        w, h = self.size
        sw, sh = screen_size
        ox, oy = self.offset

        if self.get_flag(self.flags.ANCHOR_TOP_LEFT):
            x, y = ox, oy
        elif self.get_flag(self.flags.ANCHOR_TOP_CENTER):
            x, y = sw // 2 - w // 2 - ox, oy
        elif self.get_flag(self.flags.ANCHOR_TOP_RIGHT):
            x, y = sw - w - ox, oy
        elif self.get_flag(self.flags.ANCHOR_CENTER):
            x, y = sw // 2 - w // 2 - ox, sh // 2 - h // 2 - oy
        elif self.get_flag(self.flags.ANCHOR_BOTTOM_LEFT):
            x, y = ox, sh - h - oy
        elif self.get_flag(self.flags.ANCHOR_BOTTOM_CENTER):
            x, y = sw // 2 - w // 2 - ox, sh - h - oy
        elif self.get_flag(self.flags.ANCHOR_BOTTOM_RIGHT):
            x, y = sw - w - ox, sh - h - oy

        if self.font:
            tw, th = self.font.size(self.text)
            if self.get_flag(self.flags.ALIGN_LEFT):
                x += tw
            elif self.get_flag(self.flags.ALIGN_RIGHT):
                x -= tw
            elif self.get_flag(self.flags.ALIGN_CENTER):
                x -= tw // 2
                y -= th // 2

        return [x, y]
    
    def update(self, events: BOXevents) -> None:
        for element in self.elements.values():
            element.update(events)

            mw = point_inside(
                BOXmouse.pos.screen,
                [*element.get_position(self.window.screen_size), *element.size]
            )
            if not element.get_flag(element.flags.HOVERED) and mw:
                BOXmouse.Hovering = BOXelement
                element.set_flag(element.flags.HOVERED)
                element.on_hover()
            if element.get_flag(element.flags.HOVERED) and not mw:
                BOXmouse.Hovering = None
                element.rem_flag(element.flags.HOVERED)
                element.on_unhover()
            if element.get_flag(element.flags.HOVERED) and events.mouse_pressed(BOXmouse.LeftClick):
                events.mouse[BOXmouse.LeftClick] = 0    # should't need this, but fixes the element double-click issue :|
                element.on_click()

    def blit(self, window: BOXwindow) -> None:
        target = window.screen

        last_size = [0, 0]
        if self.get_flag(self.flags.SHOW_ELEMENTS):
            for i, element in enumerate(self.elements.values()):
                if self.get_flag(self.flags.DISPLAY_LIST):
                    element.offset[1] = last_size[1] * i
                pos = element.get_position(window.screen_size)

                surface = None
                if element.get_flag(element.flags.SHOW_TEXT):
                    surface = element.font.render(element.text, self.get_flag(element.flags.ANTI_ALIAS), element.text_color)

                if element.get_flag(element.flags.SHOW_SURFACE):
                    if surface:
                        s = element.surface
                        s.fill(element.color)
                        s.blit(surface, add_v2(element.text_pos, element.padding))
                        surface = s
                    else:
                        surface = element.surface
                
                if element.get_flag(element.flags.SHOW_BORDER):
                    pg.draw.rect(
                        surface=surface,
                        rect=surface.get_rect(),
                        color=element.border_color,
                        width=element.border_width,
                        border_top_left_radius=element.border_radius[0],
                        border_top_right_radius=element.border_radius[1],
                        border_bottom_left_radius=element.border_radius[2],
                        border_bottom_right_radius=element.border_radius[3]
                    )
                
                if surface:
                    target.blit(surface, pos)
                element.blit(window)
                last_size = element.size
