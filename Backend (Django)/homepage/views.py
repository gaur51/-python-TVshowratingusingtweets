from django.http import HttpResponse
from django.shortcuts import render
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import json
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login

INDEX = "final_project"

access_key = "AWS_ACCESS_KEY"
secret = "AWS_SECRET"
region_str = 'us-west-2'
es_host = "search-twitter-stream-tithm74hpqrhcvq4pljktoldwy.us-west-2.es.amazonaws.com"
auth = AWS4Auth(access_key, secret, region_str, 'es')
es = Elasticsearch(
            hosts=[{'host': es_host, 'port': 443}],
            http_auth=auth,
            use_ssl=True,
            verify_certs=True,
            connection_class=RequestsHttpConnection
)

with open("./documents/json_data_complete.txt", encoding='utf-8') as f:
    movie_data = json.loads(f.read())

with open("./documents/Rank_Result.json", encoding='utf-8') as f:
    rankings = json.loads(f.read())

with open("./documents/SentiScore2.json", encoding='utf-8') as f:
    scores = json.loads(f.read())


with open("./documents/SentiPerc.json", encoding='utf-8') as f:
    trends = json.loads(f.read())

data_by_title = dict()
for show in movie_data["tv_list"]:
    data_by_title[show["title"]] = show

data_by_genre = dict()
for show in movie_data["tv_list"]:
    genres = show["genres"]
    for genre in genres:
        l = data_by_genre.get(genre, list())
        d = dict()
        d["title"] = show["title"]
        d["description"] = show["plot_summary"]
        d["rank"] = rankings[show["title"]]["rank"]
        d["rating"] = round(rankings[show["title"]]["rating"], 2)
        d["id"] = show["id"]
        d["poster"] = show["poster"]

        l.append(d)
        data_by_genre[genre] = l

# Create your views here.
def index(request):
    return render(request, 'homepage/index.html')

def get_top(request):
    x = []
    for k, v in data_by_title.items():
        d = dict()
        d["title"] = k
        d["description"] = v["plot_summary"]
        d["rank"] = rankings[k]["rank"]
        d["rating"] = round(rankings[k]["rating"],2)
        d["id"] = v["id"]
        x.append(d)
    return HttpResponse(json.dumps(x[0]))


@csrf_exempt
def get_by_genre(request):
    data = request.POST
    query = data.get("genre")
    items = data_by_genre[query]
    items = sorted(items, key=lambda x: x["rank"])
    for i, item in enumerate(items):
        item["rank"] = i+1
    return HttpResponse(json.dumps(items))

@csrf_exempt
def get_sentiment_breakdown(request):
    data = request.POST
    query = data.get("title")
    score_val = scores[query]
    return HttpResponse(json.dumps(score_val))

@csrf_exempt
def get_data(request):
    data = request.POST
    return HttpResponse(json.dumps(data))


@csrf_exempt
def get_genres(request):
    genres = [str(x) for x in data_by_genre.keys()]
    return HttpResponse(json.dumps(genres))

@csrf_exempt
def add_user(request):
    data = request.POST
    user_name = data["username"]
    password = data["password"]
    email = data["email"]
    u = User.objects.create(
        username=user_name,
        password=password,
        email=email,
        is_active=True
    )
    u.save()
    u.set_password(password)
    u.save()
    return HttpResponse(json.dumps({"username": user_name}))

@csrf_exempt
def login_user(request):
    data = request.POST
    user_name  = data["username"]
    password = data["password"]
    u = authenticate(username=user_name, password=password)
    if u is not None:
        login(request, u)
        return HttpResponse(json.dumps({"username":u.username}))
    else:
        return HttpResponse("Unsuccessful")



@csrf_exempt
def test_user(request):
    return HttpResponse(json.dumps(request.user.is_authenticated()))


@csrf_exempt
def get_ranked(request):
    x = []
    for k, v in data_by_title.items():
        d = dict()
        d["title"] = k
        d["description"] = v["plot_summary"]
        d["rank"] = rankings[k]["rank"]
        d["rating"] = round(rankings[k]["rating"],2)
        d["id"] = v["id"]
        x.append(d)
    x = sorted(x, key=lambda x: x["rank"])
    return HttpResponse(json.dumps(x))

@csrf_exempt
def get_info(request):
    response = {}
    if request.is_ajax():
        data = request.GET
        query = data["title"]
        res = es.search(index=INDEX, size=10000, body={"query": {"match": {"text": query}}})
        response["tweets"] = res["hits"]["hits"]
        response["description"] = data_by_title[query]["plot_summary"]
        response["title"] = query
        response["id"] = data_by_title[query]["id"]
        response["Author"] = data_by_title[query]["director"]
        response["imdb_data"] = data_by_title[query]
        return HttpResponse(json.dumps(response))
    else:
        data = request.POST
        query = data.get("title")
        res = es.search(index=INDEX, size=10000, body={"query": {"match": {"text": query}}})
        response["tweets"] = res["hits"]["hits"]
        response["description"] = data_by_title[query]["plot_summary"]
        response["title"] = query
        response["id"] = data_by_title[query]["id"]
        response["Author"] = data_by_title[query]["director"]
        response["imdb_data"] = data_by_title[query]
        response["rating"] = rankings[query]["rating"]
        response["ranking"] = rankings[query]["rank"]
        return HttpResponse(json.dumps(response))

@csrf_exempt
def get_username(request):
    if request.user.is_authenticated():
        return HttpResponse(json.dumps({"username":request.user.username}))
    else:
        return HttpResponse(json.dumps({}))

@csrf_exempt
def get_tweets_for_map(request):
    data = request.POST
    response = {}
    query = data.get("title")
    res = es.search(index=INDEX, size=10000, body={"query": {"match": {"text": query}}})
    tweets = res["hits"]["hits"]
    valid_tweets = []
    for tweet in tweets:
        if not "coordinates" in tweet["_source"].keys():
            continue
        valid_tweets.append(tweet)
    response["description"] = data_by_title[query]["plot_summary"]
    response["title"] = query
    response["id"] = data_by_title[query]["id"]
    response["Author"] = data_by_title[query]["director"]
    response["tweets"] = valid_tweets
    return HttpResponse(json.dumps(response))

def get_tweets(request):
    if request.is_ajax():
        data = request.GET
        query = data["query"]
        res = es.search(index=INDEX, size=10000, body={"query": {"match": {"text": query}}})
        return HttpResponse(json.dumps(res["hits"]["hits"]))


@csrf_exempt
def get_sentiment_trends(request):
    data = request.POST
    query = data.get("title")
    return HttpResponse(json.dumps(trends[query]))

def get_tweets_distance(request):
    '''
    This function returns the tweets using a particular search query_term and
    a longitude and latitude
    :param request: Django Request object
    :return: Returns an HTTP response of the tweet results
    '''
    if request.is_ajax():
        data = request.GET
        dist = data["distance"]
        lat, long = json.loads(data["query"])
        query_term = data["query_term"]
        d = {"query": {
        "filtered": {
            "query": {
                "match": {"text": query_term}
            },
            "filter": {
                "geo_distance": {
                    "distance": dist,
                    "tweet.coordinates": {
                        "lat": lat,
                        "lon": long
                    }
                }
            }
        }
        }
             }
        res = es.search(index=INDEX, size=10000, body=d)
        return HttpResponse(json.dumps(res["hits"]["hits"]))
