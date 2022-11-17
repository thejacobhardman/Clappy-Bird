import pygame as pg
import globals as g
import scene


class Pipe(pg.sprite.Sprite):
    def __init__(self, y_side, x_offset, height):
        pg.sprite.Sprite.__init__(self)

        self.speed = 10

        self.y_side = y_side
        self.image = pg.image.load("Assets/Art/pipe.png")
        self.original_image = self.image
        if self.y_side == "top":
            self.position=g.vec((g.WIDTH+x_offset), height)
            self.image = pg.transform.rotate(self.original_image, 180)
        elif self.y_side == "bottom":
            self.position = g.vec(g.WIDTH+x_offset, height)
        self.rect = self.image.get_rect(center=self.position)
        self.vel = g.vec(-self.speed, 0)
        self.passed_player = False
        self.id = "pipe"

    def update(self):
        self.position += self.vel
        self.rect.center = self.position
        self.did_leave_screen()
        if self.position.x < scene.game_scene.player.position.x and not self.passed_player:
            scene.game_scene.player.score += 0.5
            self.passed_player = True

    def did_leave_screen(self):
        if self.position.x < -152:
            scene.game_scene.pipes.remove(self)
