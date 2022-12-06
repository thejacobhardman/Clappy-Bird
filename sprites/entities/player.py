import pygame as pg

import scene
import scripts
import globals as g


class Player(pg.sprite.Sprite):

    def __init__(self):
        pg.sprite.Sprite.__init__(self)

        self.max_speed = 5

        self.life = 4
        self.invincibility = 0

        self.frames = [
            pg.image.load("Assets/Art/Bird Sprite/frame-1.png"),
            pg.image.load("Assets/Art/Bird Sprite/frame-2.png"),
            pg.image.load("Assets/Art/Bird Sprite/frame-3.png"),
            pg.image.load("Assets/Art/Bird Sprite/frame-4.png"),
            pg.image.load("Assets/Art/Bird Sprite/frame-5.png"),
            pg.image.load("Assets/Art/Bird Sprite/frame-6.png"),
            pg.image.load("Assets/Art/Bird Sprite/frame-7.png"),
            pg.image.load("Assets/Art/Bird Sprite/frame-8.png")
        ]
        for i in range(8):
            self.frames[i] = pg.transform.scale(self.frames[i], (100, 68))
        self.frame_index = 6
        self.image = self.frames[self.frame_index]
        self.original_image = self.image
        self.position = g.vec(g.WIDTH/2-250, g.HEIGHT/2)
        self.rect = self.image.get_rect(center=self.position)
        self.vel = g.vec(0, 0)
        self.acceleration = g.vec(0, 0)
        self.score = 0
        self.key_down = False
        self.absolute_unit = False  # <- Set this to True to make the player an absolute unit
        self.clapTimer = 8

    def reset(self):
        self.position = g.vec(g.WIDTH/2-250, g.HEIGHT/2)
        self.image = pg.transform.rotate(self.original_image, 0)
        self.rect = self.image.get_rect(center=self.position)
        self.vel = g.vec(0, 0)
        self.score = 0
        self.acceleration = g.vec(0, 0)

    def handle_movement(self):
        # Constantly descending
        self.acceleration += g.vec(0, 0.25)

        # clap if instructed to clap
        with open('interactions\interactions.txt', 'r') as reader:
            if reader.readlines() == ['CLAP']:
                self.clapflap()
                with open('interactions\interactions.txt', 'w') as writer:
                    writer.write("FALL")

        if self.clapTimer > 0:
            self.clapTimer -= 1

        if self.frame_index < 6:
            self.image = scripts.animate_sprite(self.frames, self.frame_index)
            self.frame_index += 1

        if self.acceleration.length() > self.max_speed:
            self.acceleration.scale_to_length(self.max_speed)
        if self.vel.length() > self.max_speed:
            self.vel.scale_to_length(self.max_speed)

        self.vel += self.acceleration
        self.position += self.vel
        self.rect.center = self.position

    def bounce(self):
        self.acceleration += g.vec(0, -self.max_speed * 3)
        self.frame_index = 0
        if self.invincibility == 0:
            self.get_hurt(20)

    def clapflap(self):
        if self.clapTimer <= 0:
            g.jump_sound.play()
            self.acceleration += g.vec(0, -self.max_speed * 2)
            self.frame_index = 0
            self.clapTimer = 8

    def handle_collisions(self):
        if self.did_leave_bottom_screen():
            if not self.absolute_unit:
                self.bounce()
        if self.did_leave_top_screen():
            if not self.absolute_unit and self.invincibility == 0:
                self.get_hurt(20)
        if scripts.check_collisions(self, scene.game_scene.pipes) and self.invincibility == 0:
            if not self.absolute_unit:
                self.get_hurt(40)

    def isInvincible(self):
        self.invincibility -= 1

    def did_leave_top_screen(self):
        if self.position.y < 0:
            return True

    def did_leave_bottom_screen(self):
        if self.position.y > g.HEIGHT:
            return True

    def get_hurt(self, invincibility):
        self.life -= 1
        self.invincibility = invincibility
        g.death_sound.play()
        g.offset = scripts.shake()

    def update(self):
        self.handle_movement()
        self.handle_collisions()
        if self.invincibility > 0:
            self.isInvincible()

    def toggle_absolute_unit_mode(self):
        self.absolute_unit = not self.absolute_unit
