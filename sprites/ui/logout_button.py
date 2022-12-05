import scripts
from sprites.ui.button import Button
import globals as g


# Button that logs a user out and brings them to the login page
class LogoutButton(Button):

    def __init__(self, image_file, position, text=""):
        super().__init__(image_file, position, text)

    def on_click(self):
        g.logged_in = False
        g.username = ""
        g.token = ""
        g.userId = ""
        scripts.change_scene("login")
