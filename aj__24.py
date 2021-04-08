from instaloader import Instaloader, Profile
import pandas as pd
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="geoapiExercises")
L = Instaloader()
L.login("", "")
profile = Profile.from_username(L.context, "ashish_j96")
for post in profile.get_posts():
	print(profile.username)
	print("....")
	if post.location is not None:
		lat = (post.location).lat
		lng = (post.location).lng
		location = geolocator.reverse(str(lat)+","+str(lng))
		address = location.raw['address']
	
		country = address.get('country', '')
		print(country)

	