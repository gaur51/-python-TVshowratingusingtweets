#!/usr/bin/env python
from flask import Flask

application = Flask(__name__, static_url_path='/static')

@application.route('/')
def index():
    return "hello!"

if __name__ == "__main__":
    application.run(port=5001) # for prod
