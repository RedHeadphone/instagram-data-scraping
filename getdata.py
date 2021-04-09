from instaloader import Instaloader, Profile
# import pandas as pd
from dotenv import load_dotenv
import os,asyncio
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="geoapiExercises")
load_dotenv()

print(os.getenv("IGUSER"))

import firebase_admin
from firebase_admin import credentials,firestore

cred = credentials.Certificate({
    "type": "service_account",
  "project_id": "instagram-data-scraping",
  "private_key_id": os.getenv("FIREBASE_PKI"),
  "private_key": os.getenv("FIREBASE_PK").replace('\\n', '\n'),
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
data = 5000
users = {}
users_ref = db.collection(u'cloth')
docs = users_ref.stream()

for doc in docs:
    users[doc.id]=True
count = len(users.keys())

print(count)

async def checkprofile(profile,country):
    global count
    if profile.username not in users and ("India" in profile.biography or country=="India") : 
        users[profile.username]=True
        # df=df.append([[profile.username,profile.external_url,profile.biography]])
        db.collection(u'cloth').document(profile.username).set({"username":profile.username,"contact":profile.external_url,"bio":profile.biography})
        count += 1
        print('{}: {}'.format(count, profile.username))
        # c=0
        # for i in profile.get_similar_accounts():
        #     asyncio.create_task(checkprofile(i,""))
        #     c+=1
        #     if c==5:
        #         break
        if count == data:
            exit()

async def get_hashtags_posts(query):
    # global df
    posts = loader.get_hashtag_posts(query)
    for post in posts:
        profile = post.owner_profile
        try:
            if post.location is not None:
                lat = (post.location).lat
                lng = (post.location).lng
                location = geolocator.reverse(str(lat)+","+str(lng))
                address = location.raw['address']
                country = address.get('country', '')
            else:
                country=""
        except:
            country=""
        await checkprofile(profile,country)
        

async def main():
   # hashtag = "cloths"
    hashtags = ["clothes",  "clothing",  "clothingline",  "clothingbrand",  "cloth",  "clothesforsale",  "CLOTHINGSTORE","clothingcompany",  "cloths",
   "clothings",   "clothingforsale", "clothingbrands","clothesline", "clothingsale", "clothingco", "fashion"]
    do=True
    while do:
        try:
            for hashtag in hashtags:
                last=asyncio.create_task(get_hashtags_posts(hashtag))
            await last
        except:
            asyncio.sleep(10)
        #do=False

asyncio.run(main())