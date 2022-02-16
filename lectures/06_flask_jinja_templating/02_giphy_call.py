from flask import Flask, render_template
app = Flask(__name__)

import requests, json

url = 'https://api.giphy.com/v1/gifs/search?api_key='
api_key = 'fill_in_your_giphy_api_key' # normally not hard coded

@app.route('/', methods=['GET'])
def index():
    response = requests.get(url+api_key+'&limit=1&q=smiley')
    if response.ok:
        data = response.json()
        gif = { "url" : data['data'][0]['images']['original']['url'], "alt" : data['data'][0]['title'] }
        return render_template("giphy.html", gif = gif )

#if response.ok:
#    data = response.json()
#    print(json.dumps())