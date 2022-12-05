import globals as g
from scenes.menu import Menu
import sprites.entities.textbox
import sprites.ui.login_signup_button
import pygame as pg


class LoginSignup(Menu):

    def __init__(self, login):
        super().__init__([])

        if login:
            self.sprites.add(sprites.ui.text.Text(
                "Login",
                (g.WIDTH / 2, g.HEIGHT * 0.175),
                60,
                pg.Color(0, 0, 0)
            ))
            self.sprites.add(sprites.ui.scene_button.SceneButton(
                "Assets/Art/UI/Empty-Button.png",
                (g.WIDTH * 0.5, g.HEIGHT * 0.9),
                text="Signup Instead",
                load_scene="signup"
            ))
        else:
            self.sprites.add(sprites.ui.text.Text(
                "Signup",
                (g.WIDTH / 2, g.HEIGHT * 0.175),
                60,
                pg.Color(0, 0, 0)
            ))
            self.sprites.add(sprites.ui.scene_button.SceneButton(
                "Assets/Art/UI/Empty-Button.png",
                (g.WIDTH * 0.5, g.HEIGHT * 0.9),
                text="Login Instead",
                load_scene="login"
            ))

        self.sprites.add(sprites.ui.text.Text(
            "Username",
            (g.WIDTH * 0.4, g.HEIGHT * 0.4),
            20,
            pg.Color(0, 0, 0)
        ))
        self.sprites.add(sprites.ui.text.Text(
            "Password",
            (g.WIDTH * 0.4, g.HEIGHT * 0.5),
            20,
            pg.Color(0, 0, 0)
        ))

        status_text = sprites.ui.text.Text(
            "",
            (g.WIDTH * 0.5, g.HEIGHT * 0.6),
            20,
            pg.Color(0, 0, 0)
        )

        username_field = sprites.entities.textbox.TextBox((g.WIDTH * 0.45, g.HEIGHT * 0.4))
        password_field = sprites.entities.textbox.TextBox((g.WIDTH * 0.45, g.HEIGHT * 0.5), hidden_text=True)

        if login:
            button = sprites.ui.login_signup_button.LoginSignupButton(
                "Assets/Art/UI/Empty-Button.png",
                (g.WIDTH / 2, g.HEIGHT * 0.75),
                username_field=username_field,
                password_field=password_field,
                status_text=status_text,
                login=login,
                text="Login"
            )
        else:
            button = sprites.ui.login_signup_button.LoginSignupButton(
                "Assets/Art/UI/Empty-Button.png",
                (g.WIDTH / 2, g.HEIGHT * 0.75),
                username_field=username_field,
                password_field=password_field,
                status_text=status_text,
                login=login,
                text="Signup"
            )

        self.sprites.add(username_field)
        self.sprites.add(password_field)
        self.sprites.add(status_text)
        self.sprites.add(button)
