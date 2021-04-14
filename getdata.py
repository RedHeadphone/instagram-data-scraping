import requests
hashtag = "cloth"
headers = {
    'User-Agent': ''
}




def get_list(hahstag):
	r = requests.get(f"https://www.instagram.com/explore/tags/{hashtag}/?__a=1", headers=headers)
	hashtaginfo = r.json()["graphql"]

	hasht = hashtaginfo["hashtag"]["edge_hashtag_to_media"]["edges"]
	l = []
	for i in hasht:
		print(i["node"]["owner"]["id"])
		l.append(i["node"]["owner"]["id"])
	return l
	
l = get_list("cloth")


for i in l:
	r = requests.get(f"https://www.instagram.com/graphql/query/?query_hash=c9100bf9110dd6361671f113dd02e7d6&variables={user_id:{i},%22include_chaining%22:false,%22include_reel%22:true,%22include_suggested_users%22:false,%22include_logged_out_extras%22:false,%22include_highlight_reels%22:false,%22include_related_profiles%22:false}", headers=headers)
	user_info = r.json()["data"]["user"]["reel"]["owner"]
	print(user_info)
	username.append(user_info)
print(username)