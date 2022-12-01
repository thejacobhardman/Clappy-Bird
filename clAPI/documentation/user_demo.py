# The requests library is a good library for HTTP requests in Python.
# python -m pip install requests
import requests
import json
import time

api_url = "https://clap-api.herokuapp.com"
userId = ""
token = ""


# REGISTER USER
bodyData = {"username": "ExampleDude1",
            "password": "SuperSecurePass", "friendcode": "GGGGGG"}
print("\n\nREGISTER REQUEST: " + api_url + "/user/register")
print("EXAMPLE REQUEST: " + api_url + "/user/register")
print("HEADERS: " + "None")
print("REQUEST BODY:\n" + str(bodyData))
print("RESPONSE:")
response = requests.post((api_url + "/user/register"), json=bodyData)
print(json.dumps(response.json(), indent=4))
if response.status_code == 201:
    userId = response.json()["data"]["data"]["InsertedID"]
time.sleep(2)


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


# GET SINGLE
headers = {"Authorization": token}
print("\n\nGET SINGLE REQUEST: " + api_url + "/user/secure/<str:userId>")
print("EXAMPLE REQUEST: " + api_url + "/user/secure/" + str(userId))
print("HEADERS: " + "Authorization : <str:token>")
print("REQUEST BODY:\nNone")
print("RESPONSE:")
response = requests.get(api_url + "/user/secure/" +
                        str(userId), headers=headers)
print(json.dumps(response.json(), indent=4))
time.sleep(2)


# UPDATE
updateBodyData = {"username": "ExampleDude1",
                  "password": "UpdatedPassword", "friendcode": "ABCDEFGHI"}
headers = {"Authorization": token}
print("\n\nUPDATE REQUEST: " + api_url + "/user/secure/<str:userId>")
print("EXAMPLE REQUEST: " + api_url + "/user/secure/" + str(userId))
print("HEADERS: " + "Authorization : <str:token>")
print("REQUEST BODY:\n" + str(updateBodyData))
print("RESPONSE:")
response = requests.put(
    (api_url + "/user/secure/" + str(userId)), json=updateBodyData, headers=headers)
print(json.dumps(response.json(), indent=4))
time.sleep(2)


# REFRESH TOKEN
headers = {"Authorization": token}
print("\n\nREFRESH TOKEN REQUEST: " + api_url +
      "/user/secure/refresh/<str:userId>")
print("EXAMPLE REQUEST: " + api_url + "/user/secure/refresh/" + str(userId))
print("HEADERS: " + "Authorization : <str:token>")
print("REQUEST BODY:\nNone")
print("RESPONSE:")
response = requests.get(
    api_url + "/user/secure/refresh/" + str(userId), headers=headers)
print(json.dumps(response.json(), indent=4))
token = response.json()["data"]["token"]
time.sleep(2)


# GET ALL USERS
headers = {"Authorization": token}
print("\nGET ALL REQUEST: " + api_url + "/user/s2/all")
print("EXAMPLE REQUEST: " + api_url + "/user/s2/all")
print("HEADERS: " + "Authorization : <str:token>")
print("REQUEST BODY:\nNone")
print("RESPONSE:")
response = requests.get(api_url + "/user/s2/all", headers=headers)
print(json.dumps(response.json(), indent=4))
time.sleep(2)


# PING/VALIDATE TOKEN
headers = {"Authorization": token}
print("\n\nPING/VALIDATE TOKEN REQUEST: " + api_url + "/user/s2/skedaddle")
print("EXAMPLE REQUEST: " + api_url + "/user/s2/skedaddle")
print("HEADERS: " + "Authorization : <str:token>")
print("REQUEST BODY:\nNone")
print("RESPONSE:")
response = requests.get(api_url + "/user/s2/skedaddle", headers=headers)
print(json.dumps(response.json(), indent=4))
time.sleep(2)


# DELETE
headers = {"Authorization": token}
print("\n\nDELETE REQUEST: " + api_url + "/user/secure/<str:userId>")
print("EXAMPLE REQUEST: " + api_url + "/user/secure/" + str(userId))
print("HEADERS: " + "Authorization : <str:token>")
print("REQUEST BODY:\nNone")
print("RESPONSE:")
response = requests.delete(
    api_url + "/user/secure/" + str(userId), headers=headers)
print(json.dumps(response.json(), indent=4))
time.sleep(2)


user_input = input("Enter anything to exit: ")
