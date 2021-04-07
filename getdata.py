from instaloader import Instaloader, Profile
import pandas as pd

df=pd.DataFrame([["username","contact","bio"]])

loader = Instaloader()
data = 10
users = {}

def get_hashtags_posts(query):
    global df
    posts = loader.get_hashtag_posts(query)
    count = 0
    for post in posts:
        profile = post.owner_profile
        if profile.username not in users:# and ("India" in profile.biography):  #  or post.location
            users[profile.username]=True
            df=df.append([[profile.username,profile.external_url,profile.biography]])
            count += 1
            print('{}: {}'.format(count, profile.username))
            if count == data:
                break

if __name__ == "__main__":
    hashtag = "clothes"
    try:
        get_hashtags_posts(hashtag)
        df.to_csv("data.csv",index=False)
    except:
        df.to_csv("data.csv",index=False)
