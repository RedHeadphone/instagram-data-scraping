#get similar accounts

def get_similar_accounts(given_profile):
	for profile in given_profile.get_similar_accounts():
		if profile.username not in users and ("India" in profile.biography) : 
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
