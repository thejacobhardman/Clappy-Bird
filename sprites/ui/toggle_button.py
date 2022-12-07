from sprites.ui.button import Button
import scripts
import globals as g

# Button that acts as a toggle for different options
class ToggleButton(Button):

    def __init__(self, image_file, position, display_text="", option_text="", global_variable=False, original_image="", alternate_image="", function=""):
        super().__init__(image_file, position, display_text)
        self.display_text = display_text
        self.option_text = option_text
        self.global_variable = global_variable # Needs to be a boolean not a string
        self.image_file = image_file
        self.original_image = original_image
        self.alternate_image = alternate_image
        self.position = position
        self.function = function

    def update_text(self, image_file, position):
        #scripts.get_updated_global_variable(self.global_variable)
        self.global_variable = g.absolute_unit_mode # This isn't great for abstraction but it's the best I can come up with right now.
        self.display_text = (self.option_text + str(not self.global_variable))
        image_file = self.original_image if self.global_variable == True else self.alternate_image
        super().__init__(image_file, position, self.display_text)

    def on_click(self):
        self.update_text(self.image_file, self.position)
        scripts.execute_script(self.function)
