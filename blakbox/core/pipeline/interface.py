from ...globals import pg
from ...atom import BOXatom, BOXprivate
from ...utils import point_inside

from ...log import BOXlogger
from ..app.inputs import BOXmouse
from ..app.window import BOXwindow
from ..app.events import BOXevents
from ..resource import BOXelement, BOXcontainer, BOXscrollview

class BOXinterface(BOXatom):
    def __init__(self, window: BOXwindow) -> None:
        super().__init__()
        self.window: BOXwindow = window
        self.elements: dict[str, BOXelement] = {}

    def set_element(self, key: str, element: BOXelement) -> None:
        if key in self.elements: return
        self.elements[key] = element
        BOXlogger.info(f"[BOXinterface] Set element: (key){key}")
    
    def get_element(self, key: str) -> BOXelement:
        return self.elements.get(key, None)
    
    def rem_element(self, key: str) -> None:
        if key not in self.elements: return
        self.elements[key].parent = None
        del self.elements[key]
        BOXlogger.info(f"[BOXinterface] Removed element: (key){key}")

    def clear(self) -> None:
        for element in self.elements.values():
            element.parent = None
            element.clear()
        self.elements.clear()
        BOXlogger.info("[BOXinterface] Cleared all elements")

    @BOXprivate
    def update(self, events: BOXevents) -> bool:
        def handle_element(element: BOXelement) -> bool:
            if not element.get_flag(BOXelement.flags.VISIBLE):
                return False

            if element.get_flag(BOXelement.flags.SHOW_ELEMENTS):
                for child in reversed(list(element.children.values())):
                    handle_element(child)

            element.on_update(events)
            if point_inside(BOXmouse.pos.screen, [*element.absolute_pos, *element.size]):
                BOXmouse.Hovering = element
                if not element.get_flag(BOXelement.flags.HOVERED):
                    element.set_flag(BOXelement.flags.HOVERED)
                    element.on_hover()
                if events.mouse_pressed(BOXmouse.LeftClick):
                    element.set_flag(BOXelement.flags.CLICKED)
                    element.on_click()
                else:
                    element.rem_flag(BOXelement.flags.CLICKED)
                return True
            else:
                BOXmouse.Hovering = None
                if element.get_flag(BOXelement.flags.HOVERED):
                    element.rem_flag(BOXelement.flags.HOVERED)
                    element.on_unhover()
                if element.get_flag(BOXelement.flags.CLICKED):
                    if not events.mouse_pressed(BOXmouse.LeftClick):
                        element.rem_flag(BOXelement.flags.CLICKED)
                return False

        for element in reversed(list(self.elements.values())):
            element._update_hook(events)
            if handle_element(element):
                return True
        return False
    
    @BOXprivate
    def render(self) -> None:
        for element in self.elements.values():
            if isinstance(element, BOXcontainer):
                element._layout()
            element._render(self.window.screen)
