import pygame as pg
import globals as g
from scenes.menu import Menu
import sprites.entities.textbox
import sprites.ui.login_button

class LoginScreen(Menu):

    def __init__(self, spr):
        super().__init__(spr)

    def init(self):
        username_field = sprites.entities.textbox.TextBox((g.WIDTH / 2, g.HEIGHT / 2))
        password_field = sprites.entities.textbox.TextBox((g.WIDTH / 2, g.HEIGHT * 0.6))
        login = sprites.ui.login_button.LoginButton(
            "Assets/Art/UI/logintemp.png",
            (g.WIDTH/2, g.HEIGHT*0.8),
            username_field=username_field,
            password_field=password_field,
        )
        self.sprites.add(username_field)
        self.sprites.add(password_field)
        self.sprites.add(login)
