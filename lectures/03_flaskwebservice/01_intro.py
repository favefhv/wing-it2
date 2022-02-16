"""
Beschreibung
Author
Datum
"""
#https://flask.palletsprojects.com/en/2.0.x/quickstart/#a-minimal-application 
from flask import Flask   #  install the module for vs code: py -m pip install flask
app = Flask(__name__)

# AddOn: to start via vs code: 1) set environment variable: $env:FLASK_APP="01_intro.py" 2) py -m flask run
@app.route('/')
def index():
    return 'Index page'

# Step 1 - Routing and Variables Rules: https://flask.palletsprojects.com/en/2.0.x/quickstart/#routing
@app.route('/subroute')
def subroute():
    return 'Subpage'

@app.route('/hello/')
@app.route('/hello/<string:name>')
def hello(name=None):
    if name is None:
        return 'Hello Nobody!'
    else:
        return 'Hello ' + name

# Step 2 - HTTP Methods: https://flask.palletsprojects.com/en/2.0.x/quickstart/#http-methods
from flask import request

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return 'check login data'
    else:
        return 'show login form'