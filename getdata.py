from instaloader import Instaloader, Profile
from dotenv import load_dotenv
import os,asyncio
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="geoapiExercises")
load_dotenv()


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

loader = Instaloader()
loader.login(os.getenv("IGUSER"),os.getenv("IGPASSWORD"))
print(loader.test_login())
data = 5000
users = {}
users_ref = db.collection(u'cloth')
docs = users_ref.stream()
sim=[]

for doc in docs:
    users[doc.id]=True
count = len(users.keys())

print(count)

async def simpro():
    global hashtags
    while True:
        if len(sim)==0:
            await asyncio.sleep(5)
        else:
            a=sim.pop(0)
            k=0
            don=False
            for post in a.get_posts():
                for h in post.caption_hashtags:
                    if h in hashtags:
                        await checkprofile(a,"")
                        don=True
                        break
                if don:
                    break
                k+=1
                if k==4:
                    break


async def checkprofile(profile,country):
    global count
    if profile.username not in users and ("India" in profile.biography or country=="India") : 
        users[profile.username]=True
        db.collection(u'cloth').document(profile.username).set({"username":profile.username,"contact":profile.external_url,"bio":profile.biography,"followers":profile.followers})
        count += 1
        print('{}: {}'.format(count, profile.username))
        c=0
        for i in profile.get_similar_accounts():
            sim.append(i)
            c+=1
            if c==4:
                break
        if count == data:
            exit()

async def get_hashtags_posts(query):
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

hashtags = ["clothes",  "clothing",  "clothingbrand",  "cloth",  "clothesforsale",  "cloths",
   "clothings","clothingbrands","clothesline", "clothingsale"]

async def main():
    global hashtags
    do=True
    while do:
        try:
            for hashtag in hashtags:
                last=asyncio.create_task(get_hashtags_posts(hashtag))
            asyncio.create_task(simpro())
            await last
        except:
            await asyncio.sleep(10)
        #do=False

asyncio.run(main())