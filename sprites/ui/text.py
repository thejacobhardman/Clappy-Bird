import pygame as pg
import globals as g


# https://stackoverflow.com/questions/23056597/python-pygame-writing-text-in-sprite
# Basic text sprite. Allows you to add text to your scenes in scene.py.
class Text(pg.sprite.Sprite):
    def __init__(self, text, position, size, color):

        # Call the parent class (Sprite) constructor
        pg.sprite.Sprite.__init__(self)
        self.position = position
        self.font = pg.font.SysFont("Arial", size, bold=True)
        self.color = color
        self.image = self.font.render(text, True, self.color)
        self.rect = self.image.get_rect(center=self.position)

    def change_text(self, text):
        self.image = self.font.render(text, True, self.color)
        self.rect = self.image.get_rect(center=self.position)
