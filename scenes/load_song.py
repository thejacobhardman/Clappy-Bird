import scripts
from level import Level
import scene
import globals as g
import pygame as pg


# This displays a loading screen while a song is being loaded by librosa.
class LoadSong:

    def __init__(self, sprites):
        self.sprites = pg.sprite.Group(sprites)
        self.drew_load = False
        self.song = ""

    def set_song(self, song):
        self.song = song

    def init(self):
        self.drew_load = False

    def update(self):
        if not self.drew_load:
            self.sprites.draw(g.screen)
            scripts.draw_text(scripts.generate_loading_hint(), g.game_font, pg.Color(0, 0, 0), g.screen, g.WIDTH/2, g.HEIGHT/2+50)
            self.drew_load = True
        else:
            # Load music
            pg.mixer.music.load(self.song)
            pg.mixer.music.set_volume(0.5)
            song_data = Level(self.song)
            scene.game_scene.set_song(self.song, song_data)
            scripts.change_scene("difficulty")
            self.drew_load = True
