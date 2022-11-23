import scripts
import sprites.ui.button
import scene


# Button that picks a song and navigates to the loading scene
class DifficultyButton(sprites.ui.button.Button):

    def __init__(self, image_file, position, text=""):
        super().__init__(image_file, position, text)
        self.difficulty = text

    def on_click(self):
        scene.game_scene.set_difficulty(self.difficulty)
        scripts.change_scene("countdown")
