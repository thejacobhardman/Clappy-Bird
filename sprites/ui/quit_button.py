import sprites.ui.button
import pygame as pg
import sys


# Button that exits the game
class QuitButton(sprites.ui.button.Button):

    def __init__(self, image_file, position, text=""):
        super().__init__(image_file, position, text)

    def on_click(self):
        pg.quit()
        sys.exit()
