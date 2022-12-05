import sprites.ui.song_button
from os import listdir
from os.path import isfile, join
import globals as g
from scenes.menu import Menu
import math
import sprites.ui.song_arrow_button


# Custom menu that generates buttons based on the songs in the Levels directory. Note that this inherits from menu
# so that button clicking functionality works.
class CustomSongs(Menu):

    def __init__(self, sprites_param):

        self.page_num = 1
        self.all_level_paths = [f for f in listdir("CustomLevels") if isfile(join("CustomLevels", f))]
        self.max_page_num = math.ceil(len(self.all_level_paths) / 8)

        # Add the arrow buttons if there are too many songs to display on one page
        if self.max_page_num > 1:
            sprites_param.append(sprites.ui.song_arrow_button.SongArrowButton((g.WIDTH/8, g.HEIGHT/2), False))
            sprites_param.append(sprites.ui.song_arrow_button.SongArrowButton((g.WIDTH - (g.WIDTH/8), g.HEIGHT/2), True))

        super().__init__(sprites_param)

    def tab_over(self, tab_to_right):
        self.page_num += 1 if tab_to_right else -1
        if self.page_num > self.max_page_num:
            self.page_num = 1
        elif self.page_num < 1:
            self.page_num = self.max_page_num
        self.display_buttons()

    def display_buttons(self):

        # Remove all current song buttons
        for sprite in self.sprites:
            if isinstance(sprite, sprites.ui.song_button.SongButton):
                sprite.kill()

        level_paths = self.all_level_paths[((self.page_num - 1) * 8):((self.page_num - 1) * 8) + 8]

        i = 0
        song_buttons = []
        for level in level_paths:
            x_pos = g.WIDTH / 2
            if len(level_paths) > 4:
                x_pos = g.WIDTH - (g.WIDTH / 3) if i > 3 else g.WIDTH / 3

            song_buttons.append(
                sprites.ui.song_button.SongButton(
                    "Assets/Art/UI/Empty-Button.png",
                    (x_pos, (g.HEIGHT / 4) + (120 * (i % 4))),
                    text=level[:-4],
                    song="CustomLevels/" + level,
                    flag=True
                )
            )
            i += 1
        for level in song_buttons:
            self.sprites.add(level)

    def init(self):
        if not g.pg.mixer.get_busy():
            g.birds_sound.play(-1)

        self.display_buttons()
