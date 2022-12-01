# The requests library is a good library for HTTP requests in Python.
# python -m pip install requests
import requests
import json
import time

api_url = "http://localhost:8000"
userId = ""  # "63731613537de5b26c8a9b7c"
u = "HarryJ91"
p = "123456"
token = ""


# LOGIN FIRST
bodyData = {"username": u, "password": p}
response = requests.get(api_url + "/user/auth", json=bodyData)
if response.status_code == 200:
    token = response.json()["data"]["token"]
    userId = str(response.json()["data"]["data"]["id"])
time.sleep(2)


# GET ALL FOR BOARD
print("\nGET ALL REQUEST: " + api_url + "/scores/<int:leaderboard>")
print("EXAMPLE REQUEST: " + api_url + "/scores/1")
print("HEADERS: " + "None")
print("REQUEST BODY:\nNone")
print("RESPONSE:")
response = requests.get(api_url + "/scores/1")
if response.status_code == 200:
    print(json.dumps(response.json(), indent=4))
time.sleep(2)


# GET TOP 'x' BOARD
print("\n\nGET TOP 'x' BOARD REQUEST: " + api_url +
      "/scores/limit/<int:x>/<int:leaderboard>")
print("EXAMPLE REQUEST: " + api_url + "/scores/limit/3/1")
print("HEADERS: " + "None")
print("REQUEST BODY:\nNone")
print("RESPONSE:")
response = requests.get(api_url + "/scores/limit/3/1")
if response.status_code == 200:
    print(json.dumps(response.json(), indent=4))
time.sleep(2)


# POST
bodyData = {"player": userId, "username": u,
            "leaderboard": 99, "highscore": 985}
headers = {"Authorization": token}
print("\n\nPOST REQUEST: " + api_url + "/score/<str:userId>")
print("EXAMPLE REQUEST: " + api_url + "/score/" + userId)
print("HEADERS: " + "Authorization : <str:token>")
print("REQUEST BODY:\n" + str(bodyData))
print("RESPONSE:")
response = requests.post((api_url + "/score/" + userId),
                         json=bodyData, headers=headers)
print(json.dumps(response.json(), indent=4))
time.sleep(2)


# GET SINGLE
headers = {"Authorization": token}
print("\n\nGET SINGLE REQUEST: " + api_url +
      "/score/<str:userId>/<int:leaderboard>")
print("EXAMPLE REQUEST: " + api_url + "/score/" + userId + "/99")
print("HEADERS: " + "Authorization : <str:token>")
print("REQUEST BODY:\nNone")
print("RESPONSE:")
response = requests.get(api_url + "/score/" + userId + "/99", headers=headers)
print(json.dumps(response.json(), indent=4))
time.sleep(2)


# UPDATE
updateBodyData = {"player": userId, "username": u,
                  "leaderboard": 99, "highscore": 1000}
headers = {"Authorization": token}
print("\n\nUPDATE REQUEST: " + api_url +
      "/score/<str:userId>/<int:leaderboard>")
print("EXAMPLE REQUEST: " + api_url + "/score/" + userId + "/99")
print("HEADERS: " + "Authorization : <str:token>")
print("REQUEST BODY:\n" + str(updateBodyData))
print("RESPONSE:")
response = requests.put(
    (api_url + "/score/" + userId + "/99"), json=updateBodyData, headers=headers)
print(json.dumps(response.json(), indent=4))
time.sleep(2)


# DELETE
headers = {"Authorization": token}
print("\n\nDELETE REQUEST: " + api_url +
      "/score/<str:userId>/<int:leaderboard>")
print("EXAMPLE REQUEST: " + api_url + "/score/" + userId + "/99")
print("HEADERS: " + "Authorization : <str:token>")
print("REQUEST BODY:\nNone")
print("RESPONSE:")
response = requests.delete(api_url + "/score/" +
                           userId + "/99", headers=headers)
print(json.dumps(response.json(), indent=4))
time.sleep(2)

user_input = input("Enter anything to exit: ")
