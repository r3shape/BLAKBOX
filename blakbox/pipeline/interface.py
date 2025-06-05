from blakbox.globals import pg
from blakbox.atom import BOXatom
from blakbox.utils import add_v2, sub_v2, point_inside

from blakbox.app.inputs import BOXmouse
from blakbox.app.window import BOXwindow
from blakbox.app.events import BOXevents
from blakbox.resource.element import BOXelement

class BOXinterface(BOXatom):
    class flags:
        # Visual Flags
        SHOW_ELEMENTS: int = 1 << 0
        DISPLAY_LIST: int = 1 << 1

    def __init__(self, window: BOXwindow) -> None:
        super().__init__()
        self.window: BOXwindow = window
        self.elements: dict[str, BOXelement] = {}
        self.set_flag(self.flags.SHOW_ELEMENTS)

    def set_element(self, key: str, element: "BOXelement") -> None:
        if self.get_element(key): return
        self.elements[key] = element
    
    def get_element(self, key: str) -> "BOXelement":
        return self.elements.get(key, None)
    
    def rem_element(self, key: str) -> None:
        if self.get_element(key) is not None:
            elem = self.elements.pop(key)
            del elem

    def update(self, events: BOXevents) -> None:
        for element in self.elements.values():
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

    def flush(self, window: BOXwindow) -> None:
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
