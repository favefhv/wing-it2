from flask import Flask, render_template
app = Flask(__name__)

import requests
import random

def get_image(query):
    api_key = 'fill_in_your_giphy_api_key' # normally not hard coded
    url = 'https://api.giphy.com/v1/gifs/search?api_key=' + api_key
    response = requests.get(url+'&q='+query)
    gif = None
    if response.ok:
        data = response.json()
        if len(data['data']) > 0:
            gif = random.choice(data['data'])
    return { "url" : gif['images']['original']['url'], "alt" : gif['title'] }

from forms import SearchForm

@app.route('/', methods=['GET', 'POST'])
def index():
    # https://stackoverflow.com/a/61052386
    form = SearchForm(meta={'csrf': False})
    if form.validate_on_submit():
        query = form.query.data
        gif = get_image(query)
        if not gif is None:
            return render_template('gifs.html', gif = gif, form = form, no_search_result=False) 
        else:
            return render_template('gifs.html', gif = { "url" : 'static/img/no_result.gif', "alt" : 'no search result' }, form = form, no_search_result=True) 
    return render_template('gifs.html', gif = { "url" : 'static/img/giphy.gif', "alt" : 'smiley' }, form = form, no_search_result=False)

