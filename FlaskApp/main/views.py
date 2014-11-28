from . import main
import json
import urllib2
import gevent.queue as queue
import gevent.socket as socket
from flask import render_template, jsonify, request, abort
from sock_serv_client import ConnPool

pool = ConnPool(queue.Queue, socket, "/var/run/bays.socket", 5)

import shortestpath
import musichelp
import os

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

@main.route("/getguess", methods=['GET', 'POST'])
def getguess():
    if request.method == 'GET':
        usertext = request.args.get('usertext')
    else:
        usertext = request.form['usertext']
    try:
        response = pool.send_recv(usertext)
    except Exception, e:
        return jsonify({'error': 'error'})
    return jsonify({'guess': response})
