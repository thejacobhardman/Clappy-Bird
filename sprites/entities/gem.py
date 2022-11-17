import pygame as pg
import globals as g
import scripts
import scene

class Gem(pg.sprite.Sprite):
    def __init__(self, x_offset, height, top_pipe, bottom_pipe):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("Assets/Art/purpleGem.png")
        self.image = pg.transform.scale(self.image, (35,35))
        self.position=g.vec((g.WIDTH+x_offset), height)
        self.rect = self.image.get_rect(center= self.position)
        self.vert_speed = -6
        self.vel = g.vec(-g.PIPE_SPEED, self.vert_speed)
        self.id = "gem"
        self.top_pipe = top_pipe
        self.bottom_pipe = bottom_pipe

    def update(self):
        self.position += self.vel
        self.rect.center = self.position
        self.check_collisions()

    def check_collisions(self):
        if self.rect.colliderect(self.top_pipe.rect) or self.rect.colliderect(self.bottom_pipe.rect):
            self.change_direction()
        if scene.game_scene.player.rect.colliderect(self):
            self.play_collect_sound()
            scene.game_scene.player.score += 50
            scene.game_scene.gems.remove(self)
        if self.did_leave_screen():
            scene.game_scene.gems.remove(self)

    def change_direction(self):
        self.vert_speed = self.vert_speed * -1
        self.vel = g.vec(-g.PIPE_SPEED, self.vert_speed)

    def play_collect_sound(self):
        g.gem_sound.play()

    def did_leave_screen(self):
        if self.position.x < -152:
            return True