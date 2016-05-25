__author__ = 'Cecelia'
import json
import numpy
import os
import requests
import datetime
import time
from alchemyapi import AlchemyAPI
from Siyan_api_key import *

## ---------- Get Tweets ---------- ##
#r = requests.get('http://finalproject-dev.us-west-2.elasticbeanstalk.com/get_ranked')
#ranking = json.loads(r.text)
#for tv in ranking:
#    tv_name = tv['title']
#    tv_file = open(tv_name + '.json', 'w')
#    r = requests.post('http://finalproject-dev.us-west-2.elasticbeanstalk.com/get_info/', data = {'title': tv_name} )
#    if r.status_code != 200:
#        print tv_name
#        continue
#    tv_file.write(r.text)
#    tv_file.close()
## -------------------------------- ##

Today = datetime.datetime.now()

## ---------- Global Layer ---------- ##
def Get_Global_Score(data):
    tvName = data["title"]
    c_ret = 1
    c_fav = 1
    c_pop = 10000000
    globalScore = 0
    timestamps = []

    for i in range(len(data['tweets'])):
        local = 1
        local += c_ret * data['tweets'][i]['_source']['retweet_count']
        local += c_fav * data['tweets'][i]['_source']['favorite_count']

        tweet = data['tweets'][i]['_source']['text']
        globalScore += local * Get_Local_Score(tweet,tvName)
        if float(data['tweets'][i]['_source']['timestamp_ms']) / 1460230380.0 < 10:
            timestamps.append(data['tweets'][i]['_source']['timestamp_ms'])

    # ----- popular score 1 ----- #
    if len(data['tweets']) != 0:
        Max_time = max(timestamps)
        Min_time = min(timestamps)
        Max_time = datetime.datetime.utcfromtimestamp(Max_time)
        Min_time = datetime.datetime.utcfromtimestamp(Min_time)
        delta = abs(Max_time - Min_time)
        #print tvName,delta.total_seconds()
        if len(data['tweets']) == 1:
            popScore = float(1)/((Today - Max_time).total_seconds()/100)
        else:
            popScore = float(1)/((delta.total_seconds()/len(data['tweets']))+1)
        #print c_pop * popScore
        #print globalScore
        globalScore += c_pop * popScore

    # ----- popular score 2 ----- #
    #if len(data['tweets']) != 0:
    #    Avg_time = numpy.average(timestamps)
    #    Avg_date = datetime.datetime.utcfromtimestamp(Avg_time)
    #    Delta = Today - Avg_date
    #    #print Delta.total_seconds()
    #    popScore = float(1)/(Delta.total_seconds() - 2700000)
    #    print tvName,popScore
    #    print globalScore
    #    print c_pop * popScore * 100
    #    globalScore += c_pop * popScore * 1000

    # ----- popular score 3 ----- #
    #if len(data['tweets']) != 0:
    #    top = 1 + len(data['tweets'])/10
    #    timestamps.sort(reverse=True)
    #    top_Max_time = numpy.average(timestamps[0:top])
    #    popScore = numpy.sqrt(top_Max_time)
    #    print tvName,popScore
    #    globalScore *= c_pop * popScore

    # ----- popular score 4 ----- #
    #if len(data['tweets']) != 0:
    #    Max_time = max(timestamps)
    #    popScore = numpy.sqrt(Max_time)
    #    print tvName,popScore
    #    globalScore *= c_pop * Max_time

    # ----- popular score 5 ----- #
    #if len(data['tweets']) != 0:
    #    Max_time = max(timestamps)
    #    print "max",Max_time
    #    Avg_time = numpy.average(timestamps)
    #    print "avg",Avg_time
    #    popScore = float(Max_time+Avg_time)/100000
    #    print tvName,popScore
    #    globalScore *= c_pop * popScore

    # ----- AlchemyAPI sentimental scoring ----- #
    c_senti = 10000
    senti_url = '/Users/mac/Documents/PycharmProjects/Learn/SentiScore.json'
    file = open(senti_url,'r')
    SentiScore = json.loads(file.read())
    SentiScore[tvName] = numpy.log(SentiScore[tvName]+1)
    #print c_senti * SentiScore[tvName],globalScore
    globalScore += c_senti * SentiScore[tvName]
    #alchemyapi = AlchemyAPI(alchemy_api_key)
    #response = alchemyapi.sentiment("text", tweet)
    #if response['status'] == 'OK':
    #    result = response["docSentiment"]
    #    if result["type"] == "positive":
    #        localScore *= 10
    #    elif result["type"] == "negative":
    #        localScore *= 0.1
    #    '''
    #    "docSentiment": {
    #        "type": "SENTIMENT_LABEL",
    #        "score": "DOCUMENT_SENTIMENT",
    #        "mixed": "SENTIMENT_MIXED"
    #    }
    #    '''
        #print(json.dumps(result, indent=4))
        #if 'score' in response['docSentiment']:
    #else:
    #    print('Error in sentiment analysis call: ', response['statusInfo'])

    #if len(data['tweets']) != 0:
    #    globalScore /= len(data['tweets'])
    return globalScore
## ---------------------------------- ##

## ---------- Local Layer ---------- ##
def Get_Local_Score(tweet,tvName):
    localScore = 0

    # ----- #s and @s ----- #
    count_tags_ats = 0
    c_ta = 1
    for x in range(len(tweet)):
        if tweet[x] == "#" or tweet[x] == "@":
            count_tags_ats += 1
    tmp = float(count_tags_ats + 10) / 10
    localScore += c_ta * tmp

    # ----- Keywords count ----- #
    count_keywords = 0
    c_k = 1
    c_name = 10
    low_tweet = tweet.lower()
    low_name = tvName.lower()
    keywords = low_name.split(' ')
    keyword = keywords
    Initials = keywords[0][0]
    for x in range(1,len(keywords)):
        Initials += keywords[x][0]
    if "the" in keyword:
        keyword.remove("the")
    #print keywords
    key = []
    collect = 0
    for x in range(len(keyword)):
        #print keywords[x],low_tweet.count(keywords[x])
        collect += low_tweet.count(keyword[x])
        key.append((keyword[x],low_tweet.count(keyword[x])))
    collect += low_tweet.count(Initials)
    collect += c_name * low_tweet.count(low_name)
    count_keywords = float(collect)/(len(keyword)+2)
    #print count_keywords
    localScore *= c_k * count_keywords

    # ----- keyword offset ----- #
    tweet_words = low_tweet.split(' ')
    offsets = 1
    c_o = 1
    for x in range(1,len(keywords)):
        if keywords[x] in tweet_words:
            tmp = x - 1
            while not(keywords[tmp] in tweet_words) and tmp >= 0:
                tmp = tmp - 1
            if tmp >= 0 and keywords[tmp] in tweet_words:
                off = abs(tweet_words.index(keywords[x]) - tweet_words.index(keywords[tmp]))
                offsets += abs(off - abs(x - tmp))
                #print keywords[x],keywords[tmp], tweet_words
    #print offsets
    score_offset = float(1)/offsets
    localScore *= c_o * score_offset

    # ----- sentimental scoring ----- #
    if "best" in low_tweet:
        localScore *= 10

    return localScore
## --------------------------------- ##

## ---------- Ranking ---------- ##
dr = '/Users/mac/Documents/PycharmProjects/Learn/json2/'
fileNames = os.listdir(dr)
tvNames = []
tvScores = []
IMDBScores = []
IMDB = {}
IMDBVotes = {}
c_IMDB = 0.1
c_IMDBVotes = 0.1
result = {}
for i in range(len(fileNames)):
    tvname = fileNames[i][:-5]
    tvNames.append(tvname)
    tmpurl = dr+fileNames[i]
    file = open(tmpurl,'r')
    str = file.read()
    try:
        data = json.loads(str)
    except:
        print tmpurl
        continue

    # ----- Get IMDB information ----- #
    IMDB[tvname] = data["imdb_data"]["rating"]
    IMDBVotes[tvname] = data["imdb_data"]["votes"]

    tmpScore = Get_Global_Score(data)
    logScore = numpy.log10(tmpScore+1)
    if IMDBVotes.get(tvname):
        #print logScore,c_IMDBVotes * numpy.sqrt(IMDBVotes[tvname] / 1000)
        logScore += c_IMDBVotes * numpy.sqrt(IMDBVotes[tvname] / 1000)
    logScore = numpy.sqrt(logScore)*3.2
    if IMDB.get(tvname):
        Score = (logScore + c_IMDB * IMDB[tvname]) / (1 + c_IMDB)
    tvScores.append((tvname,Score))
    IMDBScores.append((tvname,IMDB[tvname]))
sorted_tvlist = sorted(tvScores, key=lambda score: score[1],reverse=True)
sorted_IMDB = sorted(IMDBScores, key=lambda score: score[1],reverse=True)

## ---------- Save Results ---------- ##
for i in range(len(sorted_tvlist)):
    tmp = {}
    tmp["rank"] = i + 1
    tmp["rating"] = sorted_tvlist[i][1]
    result[sorted_tvlist[i][0]] = tmp
outfile = open('Rank_Result.json', 'w')
outfile.write(json.dumps(result))
outfile.close()

## ---------- Print Results ---------- ##
rankings = []
# ----- print our ranking ----- #
for x in range(len(sorted_tvlist)):
    rankings.append((sorted_tvlist[x][0], " Our Rank: ", x+1, " Our Score: ", sorted_tvlist[x][1]," IMDB rating: ", IMDB[sorted_tvlist[x][0]]))
    print "Rank ", x+1, ": ", sorted_tvlist[x][0]
# ----- print IMDB ranking ----- #
for x in range(len(sorted_tvlist)):
    print "IMDB Rank ", x+1, ": ", sorted_IMDB[x][0]
# ----- print our ranking and IMDB ranking scores ----- #
for x in range(len(sorted_tvlist)):
    print rankings[x][0],rankings[x][1],rankings[x][2],rankings[x][3],rankings[x][4],rankings[x][5],rankings[x][6]
# ----- print the average score difference ----- #
Range_Social = sorted_tvlist[0][1] - sorted_tvlist[len(sorted_tvlist)-1][1]
Range_IMDB = sorted_IMDB[0][1] - sorted_IMDB[len(sorted_IMDB)-3][1]
Diff = 0
for i in range(10):
    if IMDB.get(sorted_tvlist[i][0]):
        print sorted_tvlist[i][0], sorted_tvlist[i][1], IMDB[sorted_tvlist[i][0]], (sorted_tvlist[i][1] + IMDB[sorted_tvlist[i][0]]) / 2
        Diff += abs( sorted_tvlist[i][1] - IMDB[sorted_tvlist[i][0]] ) / IMDB[sorted_tvlist[i][0]]
Diff = Diff * Range_IMDB / Range_Social
Diff /= 10
print "Average Score difference: ", Diff



#AHS = Get_Global_Score()
#print AHS
