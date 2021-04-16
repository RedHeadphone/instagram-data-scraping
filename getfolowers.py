from instaloader import Instaloader, Profile
import pandas as pd
import numpy as np
from dotenv import load_dotenv
import os
load_dotenv()
import re
from instaloader import Instaloader, Profile
loader = Instaloader()
loader.login(os.getenv("IGUSER"),os.getenv("IGPASSWORD"))
data=pd.read_csv('data.csv')

c=0
for index, row in data.iterrows():
    if np.isnan(data.loc[index,'followers']):
        data.loc[index,"followers"]= Profile.from_username(loader.context, data.loc[index,"username"]).followers


data.to_csv("data-cloth.csv")
