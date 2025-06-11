from ..globals import pg
from ..atom import BOXatom
from ..utils import add_v2, sub_v2, point_inside

from ..log import BOXlogger
from ..app.inputs import BOXmouse
from ..app.window import BOXwindow
from ..app.events import BOXevents
from ..resource import BOXelement

class BOXinterface(BOXatom):
    def __init__(self, window: BOXwindow) -> None:
        super().__init__()
        self.window: BOXwindow = window
        self.elements: dict[str, BOXelement] = {}

        self.gap: int = 0
        self.margin: list[int] = [0, 0]
        self.padding: list[int] = [0, 0]

        self._posv: list[list[int]] = []
        self._sizev: list[list[int]] = []

    def set_element(self, key: str, element: BOXelement) -> None:
        if key in self.elements: return
        self._sizev.append(element.size)
        self._posv.append(element.pos)
        self.elements[key] = element
        BOXlogger.info(f"[BOXinterface] Set element: (key){key}")
    
    def get_element(self, key: str) -> BOXelement:
        return self.elements.get(key, None)
    
    def rem_element(self, key: str) -> None:
        if key not in self.elements: return
        self._sizev.remove(self.elements[key].size)
        self._posv.remove(self.elements[key].pos)
        self.elements[key].parent = None
        del self.elements[key]
        BOXlogger.info(f"[BOXinterface] Removed element: (key){key}")

    def clear(self) -> None:
        for element in self.elements.values():
            element.parent = None
            element.clear()
        self.elements.clear()
        BOXlogger.info("[BOXinterface] Cleared all elements")

    def layout(self, offset: list[int], element: BOXelement) -> None:
        if self.get_flag(BOXelement.flags.DISPLAY_ROW):
            element.pos = add_v2(offset[:], add_v2(self.padding, self.margin))
            offset[0] += element.size[0] + self.gap
        elif self.get_flag(BOXelement.flags.DISPLAY_LIST):
            element.pos = offset[:]
            offset[1] += element.size[1] + self.gap

    def update(self, events: BOXevents) -> bool:
        def handle_element(element: BOXelement) -> bool:
            if not element.get_flag(BOXelement.flags.VISIBLE):
                return False

            if element.get_flag(BOXelement.flags.SHOW_ELEMENTS):
                for child in reversed(list(element.children.values())):
                    if handle_element(child):
                        return True

            element.on_update(events)
            if point_inside(mouse_pos, [*element.absolute_pos, *element.size]):
                if not element.get_flag(BOXelement.flags.HOVERED):
                    BOXmouse.Hovering = BOXelement
                    element.set_flag(BOXelement.flags.HOVERED)
                    element.on_hover()
                if mouse_down:
                    element.set_flag(BOXelement.flags.CLICKED)
                    element.on_click()
                else:
                    element.rem_flag(BOXelement.flags.CLICKED)
                return True
            else:
                if element.get_flag(BOXelement.flags.HOVERED):
                    BOXmouse.Hovering = None
                    element.rem_flag(BOXelement.flags.HOVERED)
                    element.on_unhover()
                if element.get_flag(BOXelement.flags.CLICKED):
                    if not mouse_down:
                        element.rem_flag(BOXelement.flags.CLICKED)
                return False

        mouse_pos = BOXmouse.pos.screen
        mouse_down = events.mouse_pressed(BOXmouse.LeftClick)

        layout_offset = [0, 0]
        for element in reversed(list(self.elements.values())):
            self.layout(layout_offset, element)
            if handle_element(element):
                return True

        return False
    
    def render(self) -> None:
        for element in self.elements.values():
            element.surface.fill(element.color)
            element._render(self.window.screen)
