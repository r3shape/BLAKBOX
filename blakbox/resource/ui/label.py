from ...globals import pg
from .element import BOXelement

class BOXlabel(BOXelement):
    def __init__(
            self,
            font: pg.Font,
            text: str = "BOXlabel",
            size: list[int] = None,
            text_pos: list[float] = [0, 0],
            text_color: list[int] = [0, 0, 0],
            **kwargs
    ) -> None:
        super().__init__(size=font.size(text) if size is None else size, **kwargs)
        self.font: pg.Font = font
        self.text: str = text
        self.text_pos: list[float] = text_pos[:]
        self.text_color: list[int] = text_color[:]

        self.set_flag(BOXelement.flags.SHOW_TEXT)

    def _render_hook(self, target: pg.Surface) -> None:
        if self.get_flag(BOXelement.flags.SHOW_TEXT):
            text_surf = self.font.render(self.text, self.get_flag(BOXelement.flags.ANTI_ALIAS), self.text_color)
            target.blit(text_surf, self.text_pos)
