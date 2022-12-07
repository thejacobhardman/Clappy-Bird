import pygame as pg
import sprites.ui.button
import sprites.ui.upload_button
import sprites.ui.paste_button
import sprites.ui.text
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

        self.loading = sprites.ui.text.Text(
                "",
                (g.WIDTH/2, g.HEIGHT/2-180),
                29,
                pg.Color(0, 0, 0)
            ),
            
        self.videoString = sprites.ui.text.Text(
                "",
                (g.WIDTH/2, g.HEIGHT/2-150),
                16,
                pg.Color(0, 0, 0)
            ),

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
                loadingtext=self.loading,
                videotext=self.videoString
            ),
        self.sprites.add(self.textBox)
        self.sprites.add(self.loading)
        self.text = pg.sprite.Group()
        self.text.add(self.loading)
        self.sprites.add(self.uploadButton)
        self.sprites.add(self.pasteButton)
        self.sprites.add(self.videoString)
        self.x = 0

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

    def update(self):
        if self.loading[0].text == "Loading...":
            self.text.draw(g.screen)
            self.text.update()
            self.uploadButton[0].isLoading = True
            if self.x >= 5 and self.loading[0].text == "Loading...":
                self.uploadButton[0].load_song()
        self.sprites.draw(g.screen)
        self.sprites.update()
        self.__handle_click()
        if self.x <= 5 and self.loading[0].text == "Loading...":
            self.x += 1