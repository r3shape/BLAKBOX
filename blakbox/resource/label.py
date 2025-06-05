from ..globals import pg
from .element import BOXelement

class BOXlabel(BOXelement):
    def __init__(
            self,
            font: pg.Font,
            size: list[int] = [0, 0],
            text: str = "BOXlabel",
            text_pos: list[float] = [0, 0],
            text_color: list[int] = [0, 0, 0],
    ) -> None:
        super().__init__(size=font.size(text) if not [*map(lambda s: s > 0, size)][0] else size)
        self.font: pg.Font = font
        self.text: str = text
        self.text_pos: list[float] = text_pos[:]
        self.text_color: list[int] = text_color[:]

        self.set_flag(BOXelement.flags.SHOW_TEXT)

    def _render_text(self) -> None:
        if self.get_flag(BOXelement.flags.SHOW_TEXT):
            text_surf = self.font.render(self.text, self.get_flag(BOXelement.flags.ANTI_ALIAS), self.text_color)
            self.surface.blit(text_surf, self.text_pos)

    def _render(self, surface):
        self._render_text()
        super()._render(surface)