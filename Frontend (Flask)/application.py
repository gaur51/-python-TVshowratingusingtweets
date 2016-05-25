#!/usr/bin/env python
from flask import Flask, render_template, Response, request, jsonify
from flask import url_for
import sys
import requests
import json

import logging
#logging.basicConfig(filename='flask.log', level=logging.DEBUG)
# logging.info('...')
# logging.error('...')
# logging.debug('...')

apibaseurl = 'http://finalproject-dev.us-west-2.elasticbeanstalk.com/'


username = None
application = Flask(__name__, static_url_path='/static')

genre_list = ["Comedy", "Drama", "Animation", "Music", "Crime", "History", "Sci-Fi", "Romance", "Fantasy", "Mystery", "Thriller", "Adventure", "Musical", "Family", "Biography", "War", "Horror", "Action"]

def getuser():
    r = requests.get(apibaseurl + 'get_username/')
    username = r.json().get("username")
    print(username)
    return username


def get_info(tv_name):
    r = requests.post(apibaseurl + 'get_info/', data = {'title': tv_name} )
    tv_json = r.json()
    tv_json['imdb_data']['poster'] = get_poster(tv_name, tv_json['imdb_data']['poster'] )
    tagline = tv_json['imdb_data']['tagline'] or "N/A"
    tv_json['imdb_data']['tagline'] = tagline if tagline[-1] != '»' else tagline[:-4]
    return tv_json

import urllib.request
import os.path
def get_poster(tv_name, poster_url):
    # set filename
    file_ext = poster_url[poster_url.rfind('.'):]
    file_ext = file_ext if len(file_ext) > 1 else ""
    filename = tv_name+file_ext
    # get file if it doesn't exist
    if not os.path.isfile(filename):
        urllib.request.urlretrieve(poster_url, "static/img/"+filename)
    print(filename)
    return filename


@application.route('/')
def index():
    return render_template('index.html', usersession = getuser())


@application.route('/ranking')
def ranking():
    # r = requests.get('http://localhost:5001/static/get_ranked.json')
    # start another flask server (in `/data-flask`) to host the json
    r = requests.get(apibaseurl + 'get_ranked/')
    json_response = r.json()
    return render_template('ranking.html', TV_list = json_response, usersession = getuser())


@application.route('/tv', methods=['GET'])
def tv():
    tv_name = request.args.get('title') or "The Big Bang Theory"
    r = requests.post(apibaseurl + 'get_sentiment_breakdown/', data = {'title': tv_name} )
    sentiment = r.json()
    return render_template('tv.html', tvinfo = get_info(tv_name), sentiment = sentiment, usersession = username)

@application.route('/search', methods=['GET', 'POST'])
def search():
    genre = request.args.get('genre')
    genre = genre if genre in genre_list else genre_list[0]
    r = requests.post(apibaseurl + 'get_by_genre/', data = {'genre': genre} )
    tv_list = r.json()
    for tv in tv_list:
        tv['poster'] = get_poster(tv["title"], tv['poster'])
    return render_template('search.html', genre = genre, tv_list = tv_list, usersession = getuser())

@application.route('/tvjson', methods=['GET'])
def tvjson():
    tv_name = request.args.get('title') or "The Big Bang Theory"
    rjson = get_info(tv_name)
    # Build HTTP JSON Response
    json_response = json.dumps(rjson) # json_response = json.dumps(r.json() )
    response = Response(json_response, content_type='application/json; charset=utf-8')
    response.headers.add('content-length',len(json_response))
    response.status_code=200
    return response


@application.route('/getsentiment.json', methods=['GET'])
def getsentiment():
    tv_name = request.args.get('title') or "The Big Bang Theory"
    genre = request.args.get('genre') or "Comedy"
    r = requests.post(apibaseurl + 'get_by_genre/', data = {'genre': genre} )
    tv_list = r.json()
    tweet_list = []
    for tv in tv_list:
        tv_name = tv["title"]
        r = requests.post(apibaseurl + 'get_tweets_for_map/', data = {'title': tv_name} )
        rjson = r.json()
        # get geo location (LngLat)
        tweet_list.extend( [tweet['_source']['coordinates']['coordinates']  for tweet in rjson['tweets'] ] )
    # Build HTTP JSON Response
    json_response = json.dumps(tweet_list)
    response = Response(json_response, content_type='application/json; charset=utf-8')
    response.headers.add('content-length',len(json_response))
    response.status_code=200
    return response


@application.route('/login', methods=['POST'])
def login():
    username = request.args.get('password') or "guest"
    password = request.args.get('username') or "1234"
    print(username)
    r = requests.post(apibaseurl + 'login_user/', data = {'password': password, 'username': username} )

    return "hello"


if __name__ == "__main__":
    application.run(debug=True) # for dev
    #application.run(host='0.0.0.0', port=5000) # for prod
