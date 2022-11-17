import pygame as pg
from abc import ABC, abstractmethod


# This class is abstract (you can't use it to make objects). You need to know what kind of button it is to handle what
# it does on click. If you need a button for a menu, try SceneButton or SongButton, or extend Button yourself.
class Button(ABC, pg.sprite.Sprite):

    def __init__(self, image_file, position, text=""):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(image_file)
        self.position = position
        self.rect = self.image.get_rect(center=self.position)
        self.text = text
        self.font = pg.font.SysFont("Arial", 30, bold=True)
        self.text_renderer = self.font.render(text, True, pg.Color(255, 255, 255))
        self.image.blit(self.text_renderer, [self.image.get_width() / 2 - self.text_renderer.get_width() / 2,
                                             self.image.get_height() / 2 - self.text_renderer.get_height() / 2])

    def click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            return True

    @abstractmethod
    def on_click(self):
        pass
