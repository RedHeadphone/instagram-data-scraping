from dotenv import load_dotenv
import os,asyncio
import requests
load_dotenv()
headers = {
    'User-Agent': ''
}
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

data = 5000
users = {}
users_ref = db.collection(u'cloth')
docs = users_ref.stream()
sim=[]

for doc in docs:
    users[doc.id]=True
count = len(users.keys())

print(count)


# async def simpro():
#     global hashtags
#     while True:
#         if len(sim)==0:
#             await asyncio.sleep(10)
#         else:
#             a=sim.pop(0)
#             k=0
#             don=False
#             for post in a.get_posts():
#                 for h in post.caption_hashtags:
#                     if h in hashtags:
#                         print("+1 from similar accounts")
#                         asyncio.create_task(checkprofile(a,""))
#                         don=True
#                         break
#                 if don:
#                     break
#                 k+=1
#                 if k==5:
#                     break


async def checkprofile(username):
    global count,headers
    r = requests.get(f"https://www.instagram.com/{username}/?__a=1", headers=headers)
    profile = r.json()["graphql"]["user"]
    if (username not in users) and ("India" in profile["biography"]) : 
        users[username]=True
        db.collection(u'cloth').document(username).set({"username":username,"contact":profile["external_url"],"bio":profile["biography"],"followers":profile["followers"]})
        count += 1
        print('{}: {}'.format(count,username))
        # c=0
        # for i in profile.get_similar_accounts():
        #     sim.append(i)
        #     c+=1
        #     if c==10:
        #         break
        if count == data:
            exit()

hashtags = ["clothes","clothing","clothingbrand","cloth","clothesforsale","cloths","clothings","clothingbrands","clothesline","clothingsale"]

async def main():
    do=True
    while do:
        try:
            for hashtag in hashtags:
                last=asyncio.create_task(get_hashtags_posts(hashtag))
            await last
        except:
            await asyncio.sleep(10)

asyncio.run(main())
