from gevent import monkey
from . import main
import requests
import json
import urllib2
import struct
import greenlet
import gevent.socket as socket
from flask import render_template, jsonify, request, abort

import shortestpath
import musichelp
import os

monkey.patch_all()

@main.route("/chart")
def chart():
    return render_template('chart.html')

@main.route("/")
def default():
    return render_template('home.html')

@main.route("/green")
def greencheck():
    return requests.get('http://python.org').content
    #return str(greenlet.getcurrent())

@main.route("/getguess")
def getpath():
    usertext = request.args.get('usertext')
    """
    header = {'Content-Type': 'application/x-www-form-urlencoded'}
    fastcgi_req = urllib2.Request("http://localhost:8080", usertext, header)
    response = urllib2.urlopen(fastcgi_req)
    return jsonify({'guess': response.read()})

    """
    message = "{}{}".format(struct.pack("I", len(usertext)), usertext)
    sock = socket.socket(socket.AF_UNIX)
    ret = sock.connect("/var/run/bays2.socket")
    sock.send(message)
    resp = sock.recv(100)
    sock.close()
    return jsonify({'guess': resp})

