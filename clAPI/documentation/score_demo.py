# The requests library is a good library for HTTP requests in Python.
# python -m pip install requests
import requests
import json
import time

api_url = "http://localhost:8000"
userId = "6364208b9761cecb7c2b305d"

# GET ALL
print("\nGET ALL REQUEST: " + api_url + "/scores/<int:leaderboard>")
print("EXAMPLE REQUEST: " + api_url + "/scores/1")
print("REQUEST BODY:\nNone")
print("RESPONSE:")
response = requests.get(api_url + "/scores/1")
if response.status_code == 200:
    print(json.dumps(response.json(), indent=4))
time.sleep(2)


# POST
bodyData = {"player": userId,
            "leaderboard": 1, "highscore": 985}
print("\n\nPOST REQUEST: " + api_url + "/score")
print("EXAMPLE REQUEST: " + api_url + "/score")
print("REQUEST BODY:\n" + str(bodyData))
print("RESPONSE:")
response = requests.post((api_url + "/score"), json=bodyData)
print(json.dumps(response.json(), indent=4))
time.sleep(2)


# GET SINGLE
print("\n\nGET SINGLE REQUEST: " + api_url +
      "/score/<str:userId>/<int:leaderboard>")
print("EXAMPLE REQUEST: " + api_url + "/score/" + userId + "/1")
print("REQUEST BODY:\nNone")
print("RESPONSE:")
response = requests.get(api_url + "/score/" + userId + "/1")
print(json.dumps(response.json(), indent=4))
time.sleep(2)


# UPDATE
updateBodyData = {"player": userId,
                  "leaderboard": 1, "highscore": 1000}
print("\n\nUPDATE REQUEST: " + api_url +
      "/score/<str:userId>/<int:leaderboard>")
print("EXAMPLE REQUEST: " + api_url + "/score/" + userId + "/1")
print("REQUEST BODY:\n" + str(updateBodyData))
print("RESPONSE:")
response = requests.put(
    (api_url + "/score/" + userId + "/1"), json=updateBodyData)
print(json.dumps(response.json(), indent=4))
time.sleep(2)


# DELETE
print("\n\nDELETE REQUEST: " + api_url +
      "/score/<str:userId>/<int:leaderboard>")
print("EXAMPLE REQUEST: " + api_url + "/score/" + userId + "/1")
print("REQUEST BODY:\nNone")
print("RESPONSE:")
response = requests.delete(api_url + "/score/" + userId + "/1")
print(json.dumps(response.json(), indent=4))
time.sleep(2)

user_input = input("Enter anything to exit: ")
