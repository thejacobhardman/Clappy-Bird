import sprites.ui.song_button
from os import listdir
from os.path import isfile, join
import globals as g
from scenes.menu import Menu
import math
import sprites.ui.arrow_button
import pygame as pg
import requests
import json


class Leaderboard(Menu):

    def __init__(self):

        sprites_param = []

        self.page_num = 1
        self.all_level_paths = []
        for i in g.songs:
            self.all_level_paths.append(i)
            print(i)
        self.max_page_num = len(self.all_level_paths)

        # Add back button
        sprites_param.append(sprites.ui.scene_button.SceneButton(
                "Assets/Art/UI/Empty-Button.png",
                (g.WIDTH/2, g.HEIGHT*0.85),
                text="Back",
                load_scene="main_menu"
            ))

        # Add the arrow buttons if there are too many songs to display on one page
        if self.max_page_num > 1:
            sprites_param.append(sprites.ui.arrow_button.ArrowButton(
                (g.WIDTH / 8, g.HEIGHT / 2),
                menu="leaderboard",
                facing_right=False
            ))
            sprites_param.append(sprites.ui.arrow_button.ArrowButton(
                (g.WIDTH - (g.WIDTH / 8), g.HEIGHT / 2),
                menu="leaderboard",
                facing_right=True))

        super().__init__(sprites_param)

    def tab_over(self, tab_to_right):
        self.page_num += 1 if tab_to_right else -1
        if self.page_num > self.max_page_num:
            self.page_num = 1
        elif self.page_num < 1:
            self.page_num = self.max_page_num
        self.display_leaderboard()

    def display_leaderboard(self):

        response = requests.get(g.api_url + "/scores/limit/10/1")
        if response.status_code == 200:
            print(json.dumps(response.json(), indent=4))

        # I regret to inform you that Lad Boi Johnson I and II have tragically passed away in a terrible accident
        player_scores = [
            ["Lad Boi Johnson III", 5000],
            ["Lad Boi Johnson IV", 4500],
            ["Lad Boi Johnson V", 4000],
            ["Lad Boi Johnson VI", 3500],
            ["Lad Boi Johnson VII", 3000],
            ["Lad Boi Johnson VIII", 2500],
            ["Lad Boi Johnson IX", 2000],
            ["Lad Boi Johnson X", 1500],
            ["Lad Boi Johnson XI", 1000],
            ["Lad Boi Johnson XII", 500]
        ]

        # Remove all text sprites
        for sprite in self.sprites:
            if isinstance(sprite, sprites.ui.text.Text):
                sprite.kill()

        lb_sprites = []
        lb_sprites.append(sprites.ui.text.Text(
            "[Song " + str(self.page_num) + " Name Here]",
            (g.WIDTH * 0.5, g.HEIGHT * 0.15),
            50,
            pg.Color(0, 0, 0)
        ))

        for i in range(len(player_scores)):
            lb_sprites.append(sprites.ui.text.Text(
                player_scores[i][0],
                (g.WIDTH * 0.3, g.HEIGHT * (0.25 + ((i + 1) * 0.04))),
                20,
                pg.Color(0, 0, 0)
            ))

        for i in range(10):
            lb_sprites.append(sprites.ui.text.Text(
                ". . . . . . . . . . . . . . . . . . . . . . . . . .",
                (g.WIDTH * 0.5, g.HEIGHT * (0.25 + ((i + 1) * 0.04))),
                20,
                pg.Color(0, 0, 0)
            ))

        for i in range(len(player_scores)):
            lb_sprites.append(sprites.ui.text.Text(
                str(player_scores[i][1]),
                (g.WIDTH * 0.7, g.HEIGHT * (0.25 + ((i + 1) * 0.04))),
                20,
                pg.Color(0, 0, 0)
            ))

        for i in lb_sprites:
            self.sprites.add(i)


    def init(self):
        if not g.pg.mixer.get_busy():
            g.birds_sound.play(-1)

        self.display_leaderboard()
