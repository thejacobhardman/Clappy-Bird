from sprites.ui.button import Button

# Button that acts as a toggle for different options
class AbsoluteUnitToggleButton(Button):

    def __init__(self, image_file, position, text=""):
        super().__init__(image_file, position, text)

        def on_click(self):
            print("Absolute Unit Mode!!!")
