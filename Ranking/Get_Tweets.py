import json
import numpy
import os
import requests
import datetime
import time
from alchemyapi import AlchemyAPI
from Siyan_api_key import *

## ---------- Get Tweets ---------- ##
r = requests.get('http://finalproject-dev.us-west-2.elasticbeanstalk.com/get_ranked')
ranking = json.loads(r.text)
for tv in ranking:
    tv_name = tv['title']
    tv_file = open(tv_name + '.json', 'w')
    r = requests.post('http://finalproject-dev.us-west-2.elasticbeanstalk.com/get_info/', data = {'title': tv_name} )
    if r.status_code != 200:
        print tv_name
        continue
    tv_file.write(r.text)
    tv_file.close()
