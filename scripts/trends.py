from util import *
import csv
import tweepy

api_key, api_secret, token, token_secret = loadKeys(KEY_FILE)

_auth = tweepy.OAuthHandler(api_key, api_secret)
_auth.set_access_token(token, token_secret)

api = tweepy.API(_auth)

UStrends = api.trends_place(23424977) # from the end of your code
# trends1 is a list with only one element in it, which is a
# dict which we'll put in data.
data = UStrends[0]
# grab the trends
trends = data['trends']
# grab the name from each trend
names = [trend['name'] for trend in trends]
# put all the names together with a ' ' separating them
print names
trendsName = ' '.join(names)
print(trendsName)

with open('../data/inputSuggest2.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    for ind, name in enumerate(names):
        if ind >= 15:
            break
        writer.writerow([name.replace(' ','')])