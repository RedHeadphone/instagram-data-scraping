from instaloader import Instaloader, Profile
# import pandas as pd
from dotenv import load_dotenv
import os
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="geoapiExercises")
load_dotenv()

import firebase_admin
from firebase_admin import credentials,firestore

cred = credentials.Certificate({
    "type": "service_account",
  "project_id": "instagram-data-scraping",
  "private_key_id": os.getenv("FIREBASE_PKI"),
  "private_key": os.getenv("FIREBASE_PK"),
  "client_email": "firebase-adminsdk-m62gv@instagram-data-scraping.iam.gserviceaccount.com",
  "client_id": "117155528461940603699",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-m62gv%40instagram-data-scraping.iam.gserviceaccount.com"
})
firebase_admin.initialize_app(cred)

db = firestore.client()

# df=pd.DataFrame([["username","contact","bio"]])

loader = Instaloader()
loader.login(os.getenv("IGUSER"),os.getenv("IGPASSWORD"))
data = 10
users = {}
country=""

def get_hashtags_posts(query):
    global df
    posts = loader.get_hashtag_posts(query)
    count = 0
    for post in posts:
        profile = post.owner_profile
        if post.location is not None:
            lat = (post.location).lat
            lng = (post.location).lng
            location = geolocator.reverse(str(lat)+","+str(lng))
            address = location.raw['address']
	        country = address.get('country', '')
        else:
            country=""
        if profile.username not in users and ("India" in profile.biography or country="India") : 
            users[profile.username]=True
            # df=df.append([[profile.username,profile.external_url,profile.biography]])
            db.collection(u'cloth').document(profile.username).set({"username":profile.username,"contact":profile.external_url,"bio":profile.biography})
            count += 1
            print('{}: {}'.format(count, profile.username))
            if count == data:
                break

if __name__ == "__main__":
    hashtag = "cloths"
    get_hashtags_posts(hashtag)
