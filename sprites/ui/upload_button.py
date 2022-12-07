import sprites.ui.button
import sprites.entities.textbox
import scenes.upload
import youtubeDl

# Button that picks a song and navigates to the loading scene


class UploadButton(sprites.ui.button.Button):

    def __init__(self, image_file, position, text="", textBox=None, loadingtext=None, videotext=None):
        super().__init__(image_file, position, text)
        self.textBox = textBox
        self.loadingtext = loadingtext
        self.videotext = videotext
        self.isLoading = False

    def on_click(self):
        if not self.isLoading:
            self.loadingtext[0].change_text("Loading...")

    def load_song(self):
        if self.isLoading and self.loadingtext[0].text == "Loading...":
            self.loadingtext[0].change_text("Loading...done.")
            self.videotext[0].change_text(youtubeDl.yt_download(self.textBox.getText()))
            self.textBox.text = ''
