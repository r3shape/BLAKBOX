import blakbox

class PlayButton(blakbox.resource.BOXelement):
    def __init__(self, scene, font) -> None:
        super().__init__(font=font, size=[64, 32], pos=[0, 0], color=[200, 200, 200])
        self.scene = scene
        self.text = "Play"
        
        self.padding = [6, 8]
        self.offset = [0, 0]
        
        self.border_width = 2
        self.border_color = [0, 0, 0]

        self.set_flag(self.flags.SHOW_BORDER)
        self.set_flag(self.flags.ANCHOR_CENTER)

    def on_click(self):
        self.scene.app.set_scene("Main")
    
    def on_hover(self):
        self.color = [180, 180, 180]
        self.border_color = [20, 20, 20]

    def on_unhover(self):
        self.color = [200, 200, 200]
        self.border_color = [0, 0, 0]
