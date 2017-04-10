import tweepy
import json
import re

access_token = "3581919021-mS6wdcsvSaecYc1uWYiXpewSxi7jFBJJKN9393U"
access_token_secret = "0fmE8JzbJwDrp3l5SBLSLhqzsYbiYHh0jNFhbJ1FFkVId"
consumer_key = "tVacHH2m7cuZ5T0iJFlfTUmaU"
consumer_secret = "2zADWfnbutDzZj8Sic2qfZA52hGQlPk59x4GAbzJatk2tC3vUK"
 
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

string_query = "'Alzheimer' OR 'Alzheimer's' OR '#Alzheimer' OR 'lymphoma'"
string_query_bis = string_query.replace('"','')
string_query_bis = string_query_bis.replace("'", "")
string_query_list = string_query_bis.split(' OR ')

of = open('hoooola.txt', 'w')

catch_msg = [['description','message message message message message message']]
for tweet in tweepy.Cursor(api.search, q=string_query, lang="en").items():
	message = tweet.text.encode("ascii","ignore")
	description = tweet.user.description.encode("ascii","ignore")
	user_name = tweet.user.screen_name.encode("ascii","ignore")
	created_at = str(tweet.created_at)
	go = False
	query = ''
	for q in string_query_list:
		if q in message:
			query = q
			go = True
	if go is True:
		message = re.sub('^RT \S+\s+','',message)
		message = message.replace('\n', '. ')
		description = description.replace('\n', '. ')
		description = str(description).strip().lower()
		message = str(message).strip().lower()
		Forbidden = False
		if len(message) >= 35:
			for i in catch_msg:
				if i[1][:35] == message[:35]:
					Forbidden = True
			if Forbidden == False:
				one_result = []
				one_result.append(description)
				one_result.append(message)
				catch_msg.append(one_result)
				result = dict()
				result['user_name'] = user_name
				result['user_description'] = description
				result['created_at'] = created_at
				result['message'] = message
				result['source'] = 'twitter'
				result['query'] = query
				if len(result['message']) > 7:
					r = json.dumps(result, ensure_ascii=False)
					print r





