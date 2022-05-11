#! /usr/bin/env pyhon3
import requests
from config import token, user_id, server, limit
from datetime import datetime, timezone
from time import sleep
from sys import exit
from progressbar import progressbar


def get_active_user(auth_header):
    users = []
    offset = 0
    count = 100

    url = "{}/api/v1/users.list".format(server)
    while True:
        r = requests.get(url,
                headers=auth_header,
                params = {"count":100,"offset": offset},
                )

        if r.status_code == 200:
            resp = r.json()
            users += resp["users"]
            if count*offset < resp["total"]:
                offset += count
            else:
                break
        else:
            print(r.json())
            exit()
   
    active =  [u for u in users if u["active"]]
    print(f"Active users: {len(active)} out of {len(users)}")
    return active



def get_user_info(user_list, auth_header):
    url = "{}/api/v1/users.info".format(server)
    data = []
    now = datetime.now(timezone.utc)
    for user in progressbar(user_list):
        params = {"userId": user["_id"]}
        r = requests.get(url, params=params, headers=auth_header)
        sleep(1)  # beware of rate-limiting
        try:
            response = r.json()["user"]
        except KeyError:
            print(r.json())
            continue

        try:
            tmp = {"name": response["username"], "lastLogin": response["lastLogin"]}
        except KeyError:
            # new user have no "lastLogin" field before their first login, so we use the creation date
            tmp = {"name": response["username"], "lastLogin": response["createdAt"]}

        diff = abs(datetime.strptime(tmp["lastLogin"], "%Y-%m-%dT%H:%M:%S.%f%z") - now).days
        if diff >= limit:
            data.append(tmp)

    return data

def format_datetime(d):
    return datetime.fromisoformat(d.strip("Z")).strftime("%d.%m.%Y")

if __name__ == "__main__":
    auth_header = {"X-Auth-Token": token, "X-User-Id": user_id}
    user_list = get_active_user(auth_header)
    print("{} of them are active".format(len(user_list)))
    if len(user_list) > 0:
        user_info = get_user_info(user_list, auth_header)
        user_info.sort(key=lambda item: item["lastLogin"], reverse=True)
        for u in user_info:
            print("{:<20} - {}".format(u["name"], format_datetime(u["lastLogin"])))
