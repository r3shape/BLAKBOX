import blakbox

class PlayButton(blakbox.resource.BOXelement):
    def __init__(self, scene) -> None:
        super().__init__(size=[64, 32], pos=[0, 0], color=[200, 200, 200])
        self.scene = scene
        
        self.border_width = 2
        self.border_color = [0, 0, 0]

    def on_click(self):
        if self.scene == self.scene.app.get_scene("Main"):
            self.scene.app.set_scene("Launcher")
        else:
            self.scene.app.set_scene("Main")
    
    def on_hover(self):
        self.color = [180, 180, 180]
        self.border_color = [20, 20, 20]

    def on_unhover(self):
        self.color = [200, 200, 200]
        self.border_color = [0, 0, 0]

    def on_render(self, surface):
        surface.blit(self.scene.cache.get_surface("s1"), [8, 8])
