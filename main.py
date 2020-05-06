#! /usr/bin/env pyhon3
import requests
import json
from config import email, password, server
from pprint import pprint
from datetime import datetime, timezone
from time import sleep
from sys import exit

# Only list user who are offline for more than LIMIT days
LIMIT = 30

def login():
    p = {"user": email, "password": password}
    url = "{}/api/v1/login".format(server)
    r = requests.post(url, data=json.dumps(p))
    if r.status_code == 200:
        print("Login successful")
        data = r.json()
        return {"X-Auth-Token": data["data"]["authToken"], "X-User-Id": data["data"]["userId"]}
    else:
        print(r.json())
        exit()


def get_active_user(auth_header):
    url = "{}/api/v1/users.list".format(server)
    r = requests.get(url, headers=auth_header)
    if r.status_code == 200:
        # Only return active user
        print("Found {} user on your server".format(len(r.json()["users"])))
        return [u for u in r.json()["users"] if u["active"]]
    else:
        print(r.json())
        exit()


def get_user_info(user_list, auth_header):
    url = "{}/api/v1/users.info".format(server)
    data = []
    now = datetime.now(timezone.utc)
    for user in user_list:
        params = {"userId": user["_id"]}
        r = requests.get(url, params=params, headers=auth_header)
        sleep(5) # beware of rate-limiting
        try:
            response = r.json()["user"]
        except KeyError:
            print(r.json())
            continue

        try:
            tmp = {"name": response["username"], "lastLogin": response["lastLogin"]}
        except KeyError:
            tmp = {"name": response["username"], "lastLogin": response["createdAt"]}

        diff = abs(datetime.strptime(tmp["lastLogin"], "%Y-%m-%dT%H:%M:%S.%f%z") - now).days
        if diff >= LIMIT:
            data.append(tmp)

    return data

if __name__ == "__main__":
    auth_header = login()
    if auth_header:
        user_list = get_active_user(auth_header)
        print("{} of them are active".format(len(user_list)))
        if len(user_list) > 0:
            user_info = get_user_info(user_list, auth_header)
            user_info.sort(key=lambda item:item["lastLogin"], reverse=True)
            for u in user_info:
                print("{:<20} - {}".format(u["name"], u["lastLogin"]))
    else:
        print("Login failed")
