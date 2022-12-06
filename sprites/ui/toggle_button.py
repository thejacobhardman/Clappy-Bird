from sprites.ui.button import Button
import scripts
import globals as g

# Button that acts as a toggle for different options
class ToggleButton(Button):

    def __init__(self, image_file, position, text="", function=""):
        super().__init__(image_file, position, text)
        self.image_file = image_file
        self.position = position
        self.text = text
        self.function = function

    def update_text(self, image_file, position, text=("Absolute Unit Mode " + str(not g.absolute_unit_mode))):
        super().__init__(image_file, position, text)

    def on_click(self):
        self.update_text(self.image_file, self.position, text=("Absolute Unit Mode " + str(not g.absolute_unit_mode)))
        scripts.execute_script(self.function)
