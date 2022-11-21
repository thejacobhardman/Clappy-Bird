import pygame as pg
import sprites.ui.button
import globals as g


class Menu:

    def __init__(self, sprites):
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

    def update(self):
        self.sprites.draw(g.screen)
        self.__handle_click()
