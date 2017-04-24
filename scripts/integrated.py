import sys, os, time
import tweepy
import dataset
# from textblob import TextBlob
from sqlalchemy.exc import ProgrammingError
import json
from google.cloud import language

from googleplaces import GooglePlaces, types, lang


# from nltk.sentiment.vader import SentimentIntensityAnalyzer

###############################################################################
                                # Settings #
###############################################################################
TRACK_TERMS = ['brexit', 'article50', 'brexitday', 'brexitbegins', 'brexitcost']
CONNECTION_STRING = "sqlite:///../data/tweets.db"
DATA_DIR = "."
CSV_NAME = "brexit.csv"
TABLE_NAME = "brexit"
KEY_FILE = 'keys.json'

YOUR_API_KEY = 'AIzaSyBIUXa8vzR-pRPlFfXgiT4bIQOFIenznFo'

google_places = GooglePlaces(YOUR_API_KEY)

db = dataset.connect(CONNECTION_STRING)


# analyzer = SentimentIntensityAnalyzer()

language_client = language.Client()

###############################################################################
                                # Utils #
###############################################################################
def loadKeys(key_file):
    data = []
    with open(key_file) as data_file:
        data = json.load(data_file)

    return data["api_key"],data["api_secret"],data["token"],data["token_secret"]

def disp_to_term(msg):
    sys.stdout.write(msg + '\r')
    sys.stdout.flush()

def dumpData():
    cwd = os.getcwd()
    os.chdir(DATA_DIR)
    result = db[TABLE_NAME].all()
    dataset.freeze(result, format='csv', filename=CSV_NAME)
    os.chdir(cwd)


###############################################################################
                            # Twitter Stream API #
###############################################################################
class StreamListener(tweepy.StreamListener):

    def __init__(self, *args, **kwargs):
        tweepy.StreamListener.__init__(self, *args, **kwargs)
        self.status_count = 0

    def on_status(self, status):
        if status.retweeted or 'RT @' in status.text:
            return

        self.status_count += 1
        disp_to_term('%d tweeter status recieved' % self.status_count)

        description = status.user.description
        loc = status.user.location
        text = status.text
        coords = status.coordinates
        geo = status.geo
        name = status.user.screen_name
        user_created = status.user.created_at
        followers = status.user.followers_count
        id_str = status.id_str
        created = status.created_at
        retweets = status.retweet_count
        bg_color = status.user.profile_background_color
        # blob = TextBlob(text)
        # sent = blob.sentiment
        # vs = analyzer.polarity_scores(text)
        document = language_client.document_from_text(text)
        sent = document.analyze_sentiment().sentiment

        if geo is not None:
            geo = json.dumps(geo)

        if coords is not None:
            coords = json.dumps(coords)

        table = db[TABLE_NAME]

        # use google places api to complete user location

        try:
            if loc is not None:
                loc = str(loc.decode('utf-8'))
                print("location: ", loc, ";")
                query_result = google_places.nearby_search(location=loc)

                place = query_result.places[0]
                place.get_details()
                loc = str(place.formatted_address.decode('utf-8'))
                print("rematched location: ", loc, ";")
        except ProgrammingError as err:
            print(err)

        try:
            table.insert(dict(
                user_description=description,
                user_location=loc,
                coordinates=coords,
                text=text,
                geo=geo,
                user_name=name,
                user_created=user_created,
                user_followers=followers,
                id_str=id_str,
                created=created,
                retweet_count=retweets,
                user_bg_color=bg_color,
                # tb_polarity=sent.polarity,
                # vd_polarity=vs['compound'],
                # subjectivity=sent.subjectivity,
                sent_score=sent.score,
                sent_mag=sent.magnitude
            ))
        except ProgrammingError as err:
            print(err)

    def on_error(self, status_code):
        if status_code == 420:
            return False

def main():
    count = 1
    while True:
        try:
            print('Authorizing credentials...')
            api_key, api_secret, token, token_secret = loadKeys(KEY_FILE)

            auth = tweepy.OAuthHandler(api_key, api_secret)
            auth.set_access_token(token, token_secret)

            print('Success! Initializing Stream...')
            stream_listener = StreamListener()
            stream = tweepy.Stream(auth, stream_listener)
            stream.filter(track=TRACK_TERMS)
        except KeyboardInterrupt:
            print('\nDumping Data...')
            dumpData()
            break
        except Exception as e:
            count *= 2
            print('Problem encountered:')
            print(e)
            print('Retrying after %d ms...' % count)
            time.sleep(count)

if __name__ == '__main__':
    main()