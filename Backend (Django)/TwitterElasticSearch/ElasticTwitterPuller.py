from datetime import datetime
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
from tweepy import OAuthHandler
from tweepy import Stream
from settings import access_key, region_str, secret, es_host, t_api_key, t_api_secret, t_access_token, t_access_secret
from TwitterListener import TwitterListener, tweet_mapping



if __name__ == '__main__':
    print("Beginning twitter hose population")
    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = TwitterListener()
    top_tv_shows = []
    with open("./top_tv.csv") as f:
        for line in f.readlines():
            items = [x.strip() for x in line.split(",")]
            title, show_id, url = items
            top_tv_shows.append(title)
    auth = OAuthHandler(t_api_key, t_api_secret)
    auth.set_access_token(t_access_token, t_access_secret)
    stream = Stream(auth, l)

    # We remove some shows that are too short to identify well
    valid_shows = [x for x in top_tv_shows if len(x.split(" ")) > 1]
    stream.filter(track=valid_shows)


"""
l = TwitterListener()
mapping = {"tweet": tweet_mapping}


def create_index(es, index_name, mapping):
    es.indices.create(index_name, body = {'mappings': mapping})



create_index(l.es, "final_project", mapping)
"""