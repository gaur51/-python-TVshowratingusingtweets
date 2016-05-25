access_key = "AWS_ACCESS_KEY"
secret = "AWS_SECRET"
region_str = 'us-west-2'
es_host = "search-twitter-stream-tithm74hpqrhcvq4pljktoldwy.us-west-2.es.amazonaws.com"


# Twitter settings
t_api_key = "TWITTER_API_KEY"
t_api_secret = "TWITTER_API_SECRET"

t_access_token = "TWITTER_ACCESS_TOKEN"
t_access_secret = "TWITTER_ACCESS_SECRET"


tweet_mapping = {'properties':{
        'timestamp_ms': {
            'type': 'date'
        },

        'id_str': {
            'type': 'string'
        },

        'text': {
            'type': 'string'
        },
        'coordinates': {

            'type': 'geo_point'
        },

        'user': {
            'properties': {
                'id': {
                    'type': 'long'
                },
                'name': {
                    'type': 'string'
                }
            }
        }
    }
}
