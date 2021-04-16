from instaloader import Instaloader, Profile
import pandas as pd
from dotenv import load_dotenv
import os
load_dotenv()
import re
from instaloader import Instaloader, Profile
loader = Instaloader()
loader.login(os.getenv("IGUSER"),os.getenv("IGPASSWORD"))

df=pd.DataFrame([],columns=["username","contact","bio","phone_num","email","followers"])

users_ref = db.collection(u'cloth')
docs = users_ref.stream()
c=0
for doc in docs:
    de=doc.to_dict()
    lst = re.findall('\S+@\S+', de["bio"])
    k=Phonenumber.findall(de["bio"])
    de["phone_num"]=" ".join(k) if len(k)>0 else None
    de["email"]=" ".join(lst) if len(lst)>0 else None
    # try:
    #     if not ("followers" in de.keys()):
    #         de["followers"]=Profile.from_username(loader.context,de["username"]).followers
    # except:
    #     pass
    df=df.append(de,ignore_index=True)
    c+=1
print(c)
df.to_csv("data.csv")