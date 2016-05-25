"""
John Mathews
Cloud Computing and Big Data

This script populates tweets for each TV show into our database
"""


from datetime import datetime
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
from tweepy import OAuthHandler
from tweepy import Stream, API
from settings import access_key, region_str, secret, es_host, t_api_key, t_api_secret, t_access_token, t_access_secret
from TwitterListener import TwitterListener, tweet_mapping
import json


from tweepy.streaming import StreamListener, json
import time
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
from settings import access_key, region_str, secret, es_host, tweet_mapping

INDEX = "final_project"

class TwitterPopulater():

    def __init__(self):
        self.auth = AWS4Auth(access_key, secret, region_str, 'es')
        self.es = Elasticsearch(
            hosts=[{'host': es_host, 'port': 443}],
            http_auth=self.auth,
            use_ssl=True,
            verify_certs=True,
            connection_class=RequestsHttpConnection
        )


    def on_data(self, tweets):
        for doc in tweets:
            tweet = {}

            if doc.coordinates is not None:
                tweet['coordinates'] = doc.coordinates

            tweet['timestamp_ms'] = (doc.created_at - datetime(1970,1,1)).total_seconds()
            tweet["retweet_count"] = doc.retweet_count
            tweet["favorite_count"] = 1 if doc.favorited else 0
            tweet['text'] = doc.text.encode("ascii", errors="ignore")
            tweet["id_str"] = doc.id_str
            tweet['user'] = {'id': doc.author.id,
                             'name': doc.author.name}
            print(tweet)
            self.store_tweet(tweet)
        return True

    def on_error(self, status):
        print(status)

    def store_tweet(self, tweet):
        try:
            self.es.index(index=INDEX, id=tweet["id_str"], doc_type='tweet',
                          body=tweet)
        except UnicodeDecodeError:
            print("UnicodeError...skipping")



if __name__ == '__main__':
    print("Beginning twitter hose population")
    #This handles Twitter authetification and the connection to Twitter Streaming API
    p = TwitterPopulater()
    top_tv_shows = []
    with open("./top_tv.csv") as f:
        for line in f.readlines():
            items = [x.strip() for x in line.split(",")]
            title, show_id, url = items
            top_tv_shows.append(title)
    auth = OAuthHandler(t_api_key, t_api_secret)
    auth.set_access_token(t_access_token, t_access_secret)
    api = API(auth)
    valid_shows = [x for x in top_tv_shows if len(x.split(" ")) > 1]

    for show_title in valid_shows:
        results = api.search(q=show_title, count=100, language=["en"])
        p.on_data(results)


    #for result in results:
    #    print(result.text)
    #input()
    #stream = Stream(auth, l)

    # We remove some shows that are too short to identify well

    #stream.filter(track=valid_shows, languages=["en"])


"""
l = TwitterListener()
mapping = {"tweet": tweet_mapping}


def create_index(es, index_name, mapping):
    es.indices.create(index_name, body = {'mappings': mapping})



create_index(l.es, "final_project", mapping)
"""
