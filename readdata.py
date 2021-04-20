import pandas as pd
from dotenv import load_dotenv
import os
load_dotenv()
import re

Phonenumber=re.compile(r'(\+91\s\d{10}|\+91\d{10}|91\d{10}|\d{10})')
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

df=pd.DataFrame([],columns=["username","contact","bio","phone_num","email","followers"])

db = firestore.client()

users_ref = db.collection(u'cloth')
docs = users_ref.stream()
c=0
for doc in docs:
    de=doc.to_dict()
    lst = re.findall('\S+@\S+', de["bio"])
    k=Phonenumber.findall(de["bio"])
    de["phone_num"]=" ".join(k) if len(k)>0 else None
    de["email"]=" ".join(lst) if len(lst)>0 else None
    df=df.append(de,ignore_index=True)
    c+=1

print(c)
df.to_csv("data.csv",index=False)