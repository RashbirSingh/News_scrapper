#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 11:43:12 2019

@author: ubuntu
"""

import InfoScrapper
from flask import Flask, render_template, request
from flask_restful import Resource, Api
from flask import jsonify

app = Flask(__name__)
api = Api(app)

@app.route("/")
def hello(Keywords = 'Siwan'):
    result = InfoScrapper.StartFunction(Keywords)
    return jsonify(result)   

if __name__ == '__main__':
    app.run(port='5002')
    app.run(debug=True)