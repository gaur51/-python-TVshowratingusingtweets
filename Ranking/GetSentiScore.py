import requests
import json
import os
from alchemyapi import AlchemyAPI
from Siyan_api_key3 import *

dr = '/Users/mac/Documents/PycharmProjects/Learn/json2/'
fileNames = os.listdir(dr)
SentiScore = {}
for i in range(len(fileNames)):
    cnt = 0
    tvname = fileNames[i][:-5]
    tmpurl = dr+fileNames[i]
    file = open(tmpurl,'r')
    str = file.read()
    try:
        data = json.loads(str)
    except:
        print tmpurl
        continue
    pos = 0
    neu = 0
    neg = 0

    for j in range(len(data['tweets'])):
        tweet = data['tweets'][j]['_source']['text']
        if cnt < 10 and j >= 30 and j <40:
            alchemyapi = AlchemyAPI(alchemy_api_key)
            response = alchemyapi.sentiment("text", tweet)
            if response['status'] == 'OK':
                cnt += 1
                result = response["docSentiment"]
                print(json.dumps(result, indent=4))
                if result["type"] == "positive":
                    pos += 1
                elif result["type"] == "negative":
                    neg += 1
                else:
                    neu += 1
    tmp = {}
    tmp["pos"] = pos
    tmp["neg"] = neg
    tmp["neu"] = neu
    SentiScore[tvname] = tmp

outfile = open('SentiScore_3.json', 'w')
outfile.write(json.dumps(SentiScore))
outfile.close()
