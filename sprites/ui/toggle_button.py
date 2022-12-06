from sprites.ui.button import Button
import scripts

# Button that acts as a toggle for different options
class ToggleButton(Button):

    def __init__(self, image_file, position, text="", function=""):
        super().__init__(image_file, position, text)
        self.function = function

        def on_click(self):
            scripts.execute_script(self.function)
