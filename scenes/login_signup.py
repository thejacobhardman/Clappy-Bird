import globals as g
from scenes.menu import Menu
import sprites.entities.textbox
import sprites.ui.login_signup_button
import pygame as pg


class LoginSignup(Menu):

    def __init__(self, login):
        super().__init__([])
        self.login = login

    def init(self):

        if self.login:
            self.sprites.add(sprites.ui.text.Text(
                "Login",
                (g.WIDTH / 2, g.HEIGHT / 2 - 150),
                60,
                pg.Color(0, 0, 0)
            ))
            self.sprites.add(sprites.ui.scene_button.SceneButton(
                "Assets/Art/UI/Empty-Button.png",
                (g.WIDTH * 0.2, g.HEIGHT / 2),
                text="Signup Instead",
                load_scene="signup"
            ))
        else:
            self.sprites.add(sprites.ui.text.Text(
                "Signup",
                (g.WIDTH / 2, g.HEIGHT / 2 - 150),
                60,
                pg.Color(0, 0, 0)
            ))
            self.sprites.add(sprites.ui.scene_button.SceneButton(
                "Assets/Art/UI/Empty-Button.png",
                (g.WIDTH * 0.2, g.HEIGHT / 2),
                text="Login Instead",
                load_scene="login"
            ))

        self.sprites.add(sprites.ui.text.Text(
            "Username",
            (g.WIDTH * 0.4, g.HEIGHT / 2),
            20,
            pg.Color(0, 0, 0)
        ))
        self.sprites.add(sprites.ui.text.Text(
            "Password",
            (g.WIDTH * 0.4, g.HEIGHT * 0.6),
            20,
            pg.Color(0, 0, 0)
        ))

        username_field = sprites.entities.textbox.TextBox((g.WIDTH / 2, g.HEIGHT / 2))
        password_field = sprites.entities.textbox.TextBox((g.WIDTH / 2, g.HEIGHT * 0.6))

        login = sprites.ui.login_signup_button.LoginSignupButton(
            "Assets/Art/UI/logintemp.png",
            (g.WIDTH / 2, g.HEIGHT * 0.8),
            username_field=username_field,
            password_field=password_field,
            login=self.login
        )
        self.sprites.add(username_field)
        self.sprites.add(password_field)
        self.sprites.add(login)
