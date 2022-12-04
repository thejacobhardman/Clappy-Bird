import pygame as pg
import sprites.ui.button
import sprites.ui.upload_button
import sprites.entities.textbox
import globals as g
from scenes.menu import Menu


class UploadScreen(Menu):

    def __init__(self, sprites):
        super().__init__([])
        self.sprites = pg.sprite.Group(sprites)

    def __handle_click(self):
        mouseX, mouseY = pg.mouse.get_pos()
        for event in g.events:
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # self.sprites.sprites() just gets a list of sprites from the self.sprites sprite group
                    for sprite in self.sprites.sprites():
                        # Check if any buttons were clicked
                        if isinstance(sprite, sprites.ui.button.Button) and sprite.click((mouseX, mouseY)):
                            sprite.on_click()

    def init(self):
        if not g.pg.mixer.get_busy():
            g.birds_sound.play(-1)
        self.textBox = sprites.entities.textbox.TextBox((g.WIDTH/2, g.HEIGHT/2 - 300))

        self.uploadButton = sprites.ui.upload_button.UploadButton(
                "Assets/Art/UI/Empty-Button.png",
                (g.WIDTH/2+175, g.HEIGHT/2),
                text="Upload Song",
                textBox=self.textBox,
            ),
        self.sprites.add(self.textBox)
        self.sprites.add(self.uploadButton)