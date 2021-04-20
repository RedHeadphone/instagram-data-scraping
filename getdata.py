from instaloader import Instaloader, Profile,resumable_iteration
import instaloader
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
data = 1300
users = {}
users_ref = db.collection(u'kidwear')
docs = users_ref.stream()
sim=[]

for doc in docs:
    users[doc.id]=True
count = len(users.keys())
count=0
print(count)

def simpro():
    global hashtags
    if len(sim)==0:
        return
    a=sim.pop(0)
    k=0
    don=False
    for post in a.get_posts():
        for h in post.caption_hashtags:
            if h in hashtags:
                checkprofile(a,"")
                don=True
                break
        if don:
            break
        k+=1
        if k==4:
            break


def checkprofile(profile,country):
    global count
    if profile.username not in users and ("India" in profile.biography or country=="India") : 
        users[profile.username]=True
        db.collection(u'kidwear').document(profile.username).set({"username":profile.username,"link-given":profile.external_url,"bio":profile.biography,"followers":profile.followers})
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

def get_hashtags_posts(post_iterator):
    c=0
    with resumable_iteration(
            context=loader.context,
            iterator=post_iterator,
            load=lambda _, path: FrozenNodeIterator(**json.load(open(path))),
            save=lambda fni, path: json.dump(fni._asdict(), open(path, 'w')),
            format_path=lambda magic: "resume_info_{}.json".format(magic)
    ) as (is_resuming, start_index):
        for post in post_iterator:
            c+=1
            if c==20:
                return
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
            checkprofile(profile,country)
            

hashtags = ["kidsclothes","kidswear","kidsfashion","kidzfashion","kidsclothing","kidsclothesforsales","kidclothes"]

async def main():
    global hashtags
    loa=[]
    for i in hashtags:
        post_iterator = instaloader.NodeIterator(
            loader.context, "9b498c08113f1e09617a1703c22b2f32",
            lambda d: d['data']['hashtag']['edge_hashtag_to_media'],
            lambda n: instaloader.Post(loader.context, n),
            {'tag_name': i},
            f"https://www.instagram.com/explore/tags/{i}/"
        )
        loa.append(post_iterator)
    do=True
    while do:
        for i in loa:
            try:
                get_hashtags_posts(i)
                simpro()
                await asyncio.sleep(5)
            except:
                await asyncio.sleep(5)

asyncio.run(main())