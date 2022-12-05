import pygame as pg
import sprites.ui.button
import sprites.ui.upload_button
import sprites.ui.paste_button
import sprites.entities.textbox
import globals as g
from scenes.menu import Menu


class UploadScreen(Menu):

    def __init__(self, sprites):
        super().__init__(sprites)

    def init(self):
        if not g.pg.mixer.get_busy():
            g.birds_sound.play(-1)
        self.textBox = sprites.entities.textbox.TextBox((g.WIDTH/2 - 200, g.HEIGHT/2 - 90))

        self.pasteButton = sprites.ui.paste_button.PasteButton(
                "Assets/Art/UI/Empty-Button.png",
                (g.WIDTH/2 - 400, g.HEIGHT/2 - 90),
                text="Paste Link",
                textBox=self.textBox,
            ),

        self.uploadButton = sprites.ui.upload_button.UploadButton(
                "Assets/Art/UI/Empty-Button.png",
                (g.WIDTH/2+175, g.HEIGHT/2),
                text="Upload Song",
                textBox=self.textBox,
            ),
        self.sprites.add(self.textBox)
        self.sprites.add(self.uploadButton)
        self.sprites.add(self.pasteButton)