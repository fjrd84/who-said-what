#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

# Import Analyzer module:
from analyzer import *

# Import Tweepy library (Twitter API)
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

# Passwords to access Tweepy
access_token = "3581919021-mS6wdcsvSaecYc1uWYiXpewSxi7jFBJJKN9393U"
access_token_secret = "0fmE8JzbJwDrp3l5SBLSLhqzsYbiYHh0jNFhbJ1FFkVId"
consumer_key = "tVacHH2m7cuZ5T0iJFlfTUmaU"
consumer_secret = "2zADWfnbutDzZj8Sic2qfZA52hGQlPk59x4GAbzJatk2tC3vUK"


# Code for Twitter Stream Listener:

class StdOutListener(StreamListener):
    def on_data(self, data):
        result = []
        input_data = json.loads(data)
        if 'text' in input_data.keys():
            if run_analyzer(input_data['text']) != '<nothing found>':
                print run_analyzer(input_data['text'])
            return True
    def on_error(self, status):
        print status
if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    # Search words = start_words
    language_data = language_data_loader()
    stream.filter(track = language_data['start_words'])

