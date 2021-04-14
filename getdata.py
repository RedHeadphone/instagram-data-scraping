import requests

user = "linustech"

headers = {
    'User-Agent': ''
}


r = requests.get(f"https://www.instagram.com/{user}/?__a=1", headers=headers)
userinfo = r.json()["graphql"]

bio = userinfo["user"]["biography"]


print(bio)