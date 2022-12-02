import pygame as pg
import sprites.ui.button
import globals as g


# This is a class for use in scene.py which allows you to create basic menus. It expects a list of pygame sprites
# upon object creation, which it then displays when current_scene is set to this scene. This particular class has
# button clicking functionality built-in, where any sprite that inherits from the sprites.ui.button.Button class
# that is passed into this menu as one of its sprites has its on_click() method called whenever it is clicked.

# For menus where more functionality is needed, menu can be extended. Alternatively, if you have a scene that doesn't
# need buttons, you can write a new class entirely. Just make sure it has an init() and update() method. The Game class
# is a good example of this.
class Menu:

    def __init__(self, scene_sprites):
        self.sprites = pg.sprite.Group(scene_sprites)

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
