import scripts
from sprites.ui.button import Button


# Button that logs a player in
class LoginButton(Button):

    def __init__(self, image_file, position, text="", username_field=None, password_field=None):
        super().__init__(image_file, position, text)
        self.username_field = username_field
        self.password_field = password_field

    def on_click(self):
        print(self.username_field.text)
