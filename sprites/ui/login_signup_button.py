import scripts
import globals as g
import requests
import hashlib
import json
from sprites.ui.button import Button


# Button that logs a player in
class LoginSignupButton(Button):

    def __init__(self, image_file, position, text="", username_field=None, password_field=None, status_text=None,
                 login=True):
        super().__init__(image_file, position, text)
        self.username_field = username_field
        self.password_field = password_field
        self.status_text = status_text
        self.login = login

    def on_click(self):
        if self.login:
            self.login_user()
        else:
            self.signup_user()

    def login_user(self):
        bodyData = {"username": self.username_field.text,
                    "password": hashlib.sha256(self.password_field.text.encode('utf8')).hexdigest()}
        response = requests.get((g.api_url + "/user/auth"), json=bodyData)
        print(json.dumps(response.json(), indent=4))
        if response.status_code == 200:

            # Save data from HTTP response
            g.token = response.json()["data"]["token"]
            g.username = response.json()["data"]["data"]["username"]
            g.userId = response.json()["data"]["data"]["id"]
            g.logged_in = True

            print(g.token, g.username, g.userId)
            # Navigate to new menu
            scripts.change_scene("main_menu")
        elif response.status_code == 400:
            self.status_text.change_text(
                "Please enter both username and password above")
        elif response.status_code == 500:
            self.status_text.change_text("Invalid username and/or password")
        else:
            self.status_text.change_text("Failed to log in")

    def signup_user(self):
        bodyData = {"username": self.username_field.text,
                    "password": hashlib.sha256((self.password_field.text).encode('utf8')).hexdigest(),
                    "friendcode": "ABCDEF"}
        response = requests.post(
            (g.api_url + "/user/register"), json=bodyData)
        print(json.dumps(response.json(), indent=4))
        if response.status_code == 201:
            # Save data from HTTP response
            g.userId = response.json()["data"]["data"]["InsertedID"]

            print(g.userId)

            # Navigate to new menu
            scripts.change_scene("login")
        elif response.status_code == 400:
            self.status_text.change_text(
                "Please enter both username and password above")
        elif response.status_code == 500:
            self.status_text.change_text("Username provided already exists")
        else:
            self.status_text.change_text("Failed to signup")
