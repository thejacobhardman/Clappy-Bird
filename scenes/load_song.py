import scripts
from scenes.menu import Menu
from level import Level
import scene
import globals as g
import pygame as pg


class LoadSong(Menu):

    def __init__(self, sprites):
        super().__init__(sprites)
        self.drew_load = False
        self.song = ""

    def set_song(self, song):
        self.song = song

    def init(self):
        self.drew_load = False

    def update(self):
        if not self.drew_load:
            self.sprites.draw(g.screen)
            self.drew_load = True
        else:
            # Load music
            pg.mixer.music.load(self.song)
            pg.mixer.music.set_volume(0.5)
            song_data = Level(self.song)
            scene.game_scene.set_song(self.song, song_data)
            scripts.change_scene("difficulty")
            self.drew_load = True
