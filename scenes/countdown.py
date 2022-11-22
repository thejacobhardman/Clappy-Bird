import scripts
import globals as g
import pygame as pg
import sprites.ui.text


# This scene counts down from 3, and then immediately transitions to the game scene
class Countdown:

    def __init__(self):
        self.number = 3
        self.text = sprites.ui.text.Text(
                "3",
                (g.WIDTH / 2, g.HEIGHT / 2),
                60,
                pg.Color(0, 0, 0)
            )
        self.sprites = pg.sprite.Group(self.text)
        self.first_frame = True

    def init(self):
        self.first_frame = True
        self.number = 3
        self.text.change_text(str(self.number))
        pg.time.set_timer(pg.USEREVENT, 1000)
        g.countdown_sound.play()

    def update(self):
        if not self.first_frame:
            for event in g.events:
                if event.type == pg.USEREVENT:
                    self.number -= 1
                    if self.number > 0:
                        self.text.change_text(str(self.number))
                    else:
                        self.text.change_text("GO!")
            if self.number <= -1:
                scripts.change_scene("game")
        else:
            self.first_frame = False
        self.sprites.draw(g.screen)


