import pygame as pg

import scene
import scripts
import globals as g


class Player(pg.sprite.Sprite):

    def __init__(self):
        pg.sprite.Sprite.__init__(self)

        self.max_speed = 5

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

    def reset(self):
        self.position = g.vec(g.WIDTH/2-250, g.HEIGHT/2)
        self.image = pg.transform.rotate(self.original_image, 0)
        self.rect = self.image.get_rect(center=self.position)
        self.vel = g.vec(0, 0)
        self.score = 0
        self.acceleration = g.vec(0, 0)

    def handle_movement(self):
        # Constantly descending
        self.acceleration += g.vec(0, 0.4)

        # clap if instructed to clap
        with open('interactions\interactions.txt', 'r') as reader:
            if reader.readlines() == ['CLAP']:
                g.jump_sound.play()
                self.acceleration += g.vec(0, -self.max_speed * 2)
                self.frame_index = 0
                with open('interactions\interactions.txt', 'w') as writer:
                    writer.write("FALL")

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

    def handle_collisions(self):
        if self.did_leave_screen():
            g.death_sound.play()
            g.offset = scripts.shake()
            if not self.absolute_unit:
                pg.mixer.music.stop()
                pg.mixer.music.unload()
                scene.game_scene.gems.empty()
                scripts.change_scene("game_over")
        if scripts.check_collisions(self, scene.game_scene.pipes):
            g.death_sound.play()
            g.offset = scripts.shake()
            if not self.absolute_unit:
                pg.mixer.music.stop()
                pg.mixer.music.unload()
                scene.game_scene.gems.empty()
                scripts.change_scene("game_over")

    def did_leave_screen(self):
        if self.position.y > g.HEIGHT:
            return True
        if self.position.y < 0:
            return True

    def update(self):
        self.handle_movement()
        self.handle_collisions()
