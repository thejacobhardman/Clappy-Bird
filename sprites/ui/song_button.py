import scripts
import sprites.ui.button
import scene


# Button that picks a song and navigates to the loading scene.
class SongButton(sprites.ui.button.Button):

    def __init__(self, image_file, position, text="", song="", flag=None):
        super().__init__(image_file, position, text)
        self.song = song
        self.flag = flag

    def on_click(self):
        scene.scenes["load_song"].set_song(self.song)
        scene.scenes["game"].set_songFlag(self.flag)
        scripts.change_scene("load_song")
