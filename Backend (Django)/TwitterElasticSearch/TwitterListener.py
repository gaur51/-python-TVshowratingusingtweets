from tweepy.streaming import StreamListener, json
import time
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
from settings import access_key, region_str, secret, es_host, tweet_mapping

INDEX = "final_project"

class TwitterListener(StreamListener):

    def __init__(self):
        super(TwitterListener, self).__init__()
        self.auth = AWS4Auth(access_key, secret, region_str, 'es')
        self.es = Elasticsearch(
            hosts=[{'host': es_host, 'port': 443}],
            http_auth=self.auth,
            use_ssl=True,
            verify_certs=True,
            connection_class=RequestsHttpConnection
        )


    def on_data(self, data):
        data = data.decode('ascii', errors="replace")
        tweets = json.loads('[' + data + ']')
        for doc in [x for x in tweets if "text" in x.keys()]:
            tweet = {}

            if doc["coordinates"] is not None:
                tweet['coordinates'] = doc['coordinates']['coordinates']
            if "hashtags" in doc["entities"].keys():
                hashtags = [x["text"] for x in doc["entities"]["hashtags"]]
                tweet["hashtags"] = hashtags

            tweet['timestamp_ms'] = doc['timestamp_ms']
            tweet["retweet_count"] = doc["retweet_count"]
            tweet["favorite_count"] = doc["favorite_count"]
            tweet['text'] = doc['text']
            tweet["id_str"] = doc['id_str']
            tweet['user'] = {'id': doc['user']['id'],
                             'name': doc['user']['name']}
            print(tweet)
            self.store_tweet(tweet)
            time.sleep(1)
        return True

    def on_error(self, status):
        print(status)

    def store_tweet(self, tweet):
        try:
            self.es.index(index=INDEX, id=tweet["id_str"], doc_type='tweet',
                          body=tweet)
        except UnicodeDecodeError:
            print("UnicodeError")



