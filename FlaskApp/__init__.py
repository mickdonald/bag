from flask import Flask, g
from inspect import getmembers, isfunction

app = Flask(__name__)

from main import main

app.register_blueprint(main)


