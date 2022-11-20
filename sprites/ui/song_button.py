import scripts
import sprites.ui.button
import globals as g
import scene


# Button that picks a song and navigates to the loading scene
class SongButton(sprites.ui.button.Button):

    def __init__(self, image_file, position, text="", song=""):
        super().__init__(image_file, position, text)
        self.song = song

    def on_click(self):
        scene.scenes["load_song"].set_song(self.song)
        scripts.change_scene("load_song")
