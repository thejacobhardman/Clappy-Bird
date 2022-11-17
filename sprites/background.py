import pygame as pg
import globals as g


class Background(pg.sprite.Sprite):

    def __init__(self, position):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("Assets/Art/background.png").convert()
        self.position = position
        self.vel = g.vec(-4, 0)
        self.rect = self.image.get_rect(center=self.position)
        self.id = "background"

    def update(self):
        self.position += self.vel
        self.rect.center = self.position
        self.wrap_around_screen()

    def wrap_around_screen(self):
        if self.position.x < -(g.WIDTH/2 + 1920):
            self.position = g.vec(g.WIDTH/2+1900, g.HEIGHT/2)