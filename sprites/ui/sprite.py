import pygame as pg


# Basic sprite class that creates a pygame sprite. You can use this to add sprites to your menus in scenes.py.
class Sprite(pg.sprite.Sprite):

    def __init__(self, image_file, position):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(image_file)
        self.position = position
        self.rect = self.image.get_rect(center=self.position)