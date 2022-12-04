import sprites.ui.button
import sprites.entities.textbox


# Button that picks a song and navigates to the loading scene
class UploadButton(sprites.ui.button.Button):

    def __init__(self, image_file, position, text="", textBox=None):
        super().__init__(image_file, position, text)
        self.textBox = textBox

    def on_click(self):
        print(self.textBox.getText())