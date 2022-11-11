# The requests library is a good library for HTTP requests in Python.
# python -m pip install requests
import requests
import json
import time

api_url = "http://localhost:6000"

# GET ALL
print("\nGET ALL REQUEST: " + api_url + "/users")
print("EXAMPLE REQUEST: " + api_url + "/users")
print("REQUEST BODY:\nNone")
print("RESPONSE:")
response = requests.get(api_url + "/users")
if response.status_code == 200:
    print(json.dumps(response.json(), indent=4))
time.sleep(2)


# POST
bodyData = {"username": "ExampleDude1",
            "password": "SuperSecurePass", "friendcode": "ABCDEFGHI"}
print("\n\nPOST REQUEST: " + api_url + "/user")
print("EXAMPLE REQUEST: " + api_url + "/user")
print("REQUEST BODY:\n" + str(bodyData))
print("RESPONSE:")
response = requests.post((api_url + "/user"), json=bodyData)
print(json.dumps(response.json(), indent=4))
if response.status_code == 201:
    userId = response.json()["data"]["data"]["InsertedID"]
else:
    userId = 1
time.sleep(2)


# GET SINGLE
print("\n\nGET SINGLE REQUEST: " + api_url + "/user/<str:userId>")
print("EXAMPLE REQUEST: " + api_url + "/user/" + str(userId))
print("REQUEST BODY:\nNone")
print("RESPONSE:")
response = requests.get(api_url + "/user/" + str(userId))
print(json.dumps(response.json(), indent=4))
time.sleep(2)


# UPDATE
updateBodyData = {"username": "ExampleDude1",
                  "password": "UpdatedPassword", "friendcode": "ABCDEFGHI"}
print("\n\nUPDATE REQUEST: " + api_url + "/user/<str:userId>")
print("EXAMPLE REQUEST: " + api_url + "/user/" + str(userId))
print("REQUEST BODY:\n" + str(updateBodyData))
print("RESPONSE:")
response = requests.put(
    (api_url + "/user/" + str(userId)), json=updateBodyData)
print(json.dumps(response.json(), indent=4))
time.sleep(2)


# DELETE
print("\n\nDELETE REQUEST: " + api_url + "/user/<str:userId>")
print("EXAMPLE REQUEST: " + api_url + "/user/" + str(userId))
print("REQUEST BODY:\nNone")
print("RESPONSE:")
response = requests.delete(api_url + "/user/" + str(userId))
print(json.dumps(response.json(), indent=4))
time.sleep(2)

user_input = input("Enter anything to exit: ")
