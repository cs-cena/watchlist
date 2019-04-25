# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 00:40:46 2019

@author: Administrator
"""

from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Welcome to My Watchlist!'

if __name__ == '__main__':
    app.run()
