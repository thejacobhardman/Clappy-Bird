import scripts
import globals as g
import requests
import hashlib
import json
from sprites.ui.button import Button


# Button that logs a player in
class LoginSignupButton(Button):

    def __init__(self, image_file, position, text="", username_field=None, password_field=None, login=True):
        super().__init__(image_file, position, text)
        self.username_field = username_field
        self.password_field = password_field
        self.login = login

    def on_click(self):
        if self.login:
            bodyData = {"username": self.username_field.text,
                        "password": hashlib.sha256(self.password_field.text.encode('utf8')).hexdigest()}
            response = requests.get((g.api_url + "/user/auth"), json=bodyData)
            print(json.dumps(response.json(), indent=4))
            if response.status_code == 200:
                # Save data from HTTP response
                g.token = response.json()["data"]["token"]
                g.username = response.json()["data"]["data"]["username"]
                g.userId = response.json()["data"]["data"]["id"]

                print(g.token, g.username, g.userId)

                # Navigate to new menu
                scripts.change_scene("main_menu")
            else:
                print(response.status_code)
        else:
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
            else:
                print(response.status_code)


"""
# AUTHENTICATE USER/LOGIN
bodyData = {"username": "ExampleDude1", "password": "SuperSecurePass"}
print("\n\nLOGIN REQUEST: " + api_url + "/user/auth")
print("EXAMPLE REQUEST: " + api_url + "/user/auth")
print("HEADERS: " + "None")
print("REQUEST BODY:\n" + str(bodyData))
print("RESPONSE:")
response = requests.get(api_url + "/user/auth", json=bodyData)
print(json.dumps(response.json(), indent=4))
if response.status_code == 200:
    token = response.json()["data"]["token"]
time.sleep(2)

LOGIN REQUEST: https://clap-api.herokuapp.com/user/auth
EXAMPLE REQUEST: https://clap-api.herokuapp.com/user/auth
HEADERS: None
REQUEST BODY:
{'username': 'ExampleDude1', 'password': 'SuperSecurePass'}
RESPONSE:
{
    "status": 200,
    "message": "success",
    "data": {
        "data": {
            "id": "6385353508248b78796438a5",
            "username": "ExampleDude1",
            "friendcode": "GGGGGG"
        },
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNjM4NTM1MzUwODI0OGI3ODc5NjQzOGE1IiwiZXhwIjoxNjY5Njc3ODk1fQ.Mu8zVgZrEPQWpZXme2gcSKq39Khn2TCNE8HigQ_CNb8"
    }
}
"""
