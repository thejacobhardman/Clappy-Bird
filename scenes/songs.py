import sprites.ui.song_button
from os import listdir
from os.path import isfile, join
import globals as g
from scenes.menu import Menu


class Songs(Menu):

    def __init__(self, sprites):
        super().__init__(sprites)

    def init(self):
        if not g.pg.mixer.get_busy():
            g.birds_sound.play(-1)

        level_paths = [f for f in listdir("Levels") if isfile(join("Levels", f))]
        level_buttons = []
        i = 0

        for level in level_paths:
            level_buttons.append(
                sprites.ui.song_button.SongButton(
                    "Assets/Art/UI/Empty-Button.png",
                    (g.WIDTH / 2, (g.HEIGHT / 4) + (100 * i)),
                    text=level,
                    song="Levels/" + level
                )
            )
            i += 1
        for level in level_buttons:
            self.sprites.add(level)
