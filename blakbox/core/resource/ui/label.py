from ....globals import pg
from .element import BOXelement

class BOXlabel(BOXelement):
    def __init__(
            self,
            font: pg.Font,
            text: str = None,
            size: list[int] = None,
            icon: pg.Surface = None,
            icon_pos: list[float] = [0, 0],
            text_pos: list[float] = [0, 0],
            text_color: list[int] = [0, 0, 0],
            flags: int = 0,
            **kwargs
    ) -> None:
        super().__init__(size=font.size(text) if size is None else size, **kwargs)
        self.text: str = text
        self.font: pg.Font = font
        self.icon: pg.Surface = icon
        self.icon_pos: list[float] = icon_pos[:]
        self.text_pos: list[float] = text_pos[:]
        self.text_color: list[int] = text_color[:]
        self.set_flag(self.flags.SHOW_TEXT)
        self.set_flag(flags)

    def _render_hook(self, target: pg.Surface) -> None:
        if isinstance(self.text, str) and self.get_flag(BOXelement.flags.SHOW_TEXT):
            text_surf = self.font.render(self.text, self.get_flag(BOXelement.flags.ANTI_ALIAS), self.text_color)
            target.blit(text_surf, self.text_pos)

        if isinstance(self.icon, pg.Surface):
            target.blit(self.icon, self.icon_pos)
