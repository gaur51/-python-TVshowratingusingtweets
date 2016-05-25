import requests
import json
import os

dr1 = '/Users/mac/Documents/PycharmProjects/Learn/SentiScore2.json'
dr2 = '/Users/mac/Documents/PycharmProjects/Learn/SentiScore_1.json'
dr3 = '/Users/mac/Documents/PycharmProjects/Learn/SentiScore_2.json'
dr4 = '/Users/mac/Documents/PycharmProjects/Learn/SentiScore_3.json'
dr = '/Users/mac/Documents/PycharmProjects/Learn/json2/'
fileNames = os.listdir(dr)
tvNames = []
for i in range(len(fileNames)):
    tvname = fileNames[i][:-5]
    tmpurl = dr+fileNames[i]
    file = open(tmpurl,'r')
    str = file.read()
    try:
        data = json.loads(str)
        tvNames.append(tvname)
    except:
        print tmpurl
        continue
#print len(tvNames)

file = open(dr1,'r')
data1 = json.loads(file.read())
file = open(dr2,'r')
data2 = json.loads(file.read())
file = open(dr3,'r')
data3 = json.loads(file.read())
file = open(dr4,'r')
data4 = json.loads(file.read())

for i in tvNames:
    data1[i]["neg"] += data2[i]["neg"] + data3[i]["neg"] + data4[i]["neg"]
    data1[i]["pos"] += data2[i]["pos"] + data3[i]["pos"] + data4[i]["pos"]
    data1[i]["neu"] += data2[i]["neu"] + data3[i]["neu"] + data4[i]["neu"]

outfile = open('SentiScore_new.json', 'w')
outfile.write(json.dumps(data1))
outfile.close()
