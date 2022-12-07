import scripts
from sprites.ui.button import Button


# Button that navigates between scenes.
class SceneButton(Button):

    def __init__(self, image_file, position, text="", load_scene="", size=None):
        super().__init__(image_file, position, text, size=size)
        self.load_scene = load_scene

    def on_click(self):
        scripts.change_scene(self.load_scene)
