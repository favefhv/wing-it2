from flask import Flask
app = Flask(__name__)

#Step 5 - Rendering Templates: https://flask.palletsprojects.com/en/2.0.x/quickstart/#rendering-templates
from flask import render_template 

@app.route('/')
def index():
    # return "<html><head><title>Index page</title><body><h1>Index Page</h1></body></html>"
    return render_template('index.html') 

@app.route('/templates/')
@app.route('/templates/<name>')
def hello_template(name=None):
    return render_template('hello.html', name=name)

@app.errorhandler(404)
def not_found(error):
    return render_template('error.html'), 404

@app.route('/bootstrap')
def bootstrap():
    return render_template('bootstrap.html')