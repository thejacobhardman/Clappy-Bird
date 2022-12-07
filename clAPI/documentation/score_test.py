# The requests library is a good library for HTTP requests in Python.
# python -m pip install requests
import requests
import json
import time

api_url = "https://clap-api.herokuapp.com"  # "http://88.214.59.111"
userId = ""  # "63731613537de5b26c8a9b7c"
u = "HarryJ91"
p = "123456"
token = ""

bodyData = {"username": u, "password": p}
response = requests.get(api_url + "/user/auth", json=bodyData)
if response.status_code == 200:
    token = response.json()["data"]["token"]
    userId = str(response.json()["data"]["data"]["id"])
time.sleep(2)



print("\n\nGET TOP 'x' BOARD REQUEST: " + api_url +
      "/scores/limit/<int:x>/<int:leaderboard>")
print("EXAMPLE REQUEST: " + api_url + "/scores/limit/3/1")
print("HEADERS: " + "None")
print("REQUEST BODY:\nNone")
print("RESPONSE:")
response = requests.get(api_url + "/scores/limit/3/2")
if response.status_code == 200:
    print(json.dumps(response.json(), indent=4))
time.sleep(2)