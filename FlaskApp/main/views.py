from . import main
import json
import urllib2
from flask import render_template, jsonify, request, abort

import shortestpath
import musichelp
import os

@main.route("/chart")
def chart():
    return render_template('chart.html')

@main.route("/")
def default():
    return render_template('home.html')

@main.route("/getguess")
def getpath():
    usertext = '_'.join(request.args.get('usertext').split('\s'))
    header = {'Content-Type': 'application/x-www-form-urlencoded'}
    fastcgi_req = urllib2.Request("http://localhost:8080", usertext, header)
    response = urllib2.urlopen(fastcgi_req)
    return jsonify({'guess': response.read()})
