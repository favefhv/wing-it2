from flask import Flask, request
app = Flask(__name__)

# Step 3 - Return json: https://pythonise.com/series/learning-flask/flask-http-methods
from flask import jsonify

stock = {
    "fruit": {
        "apple": 30,
        "banana": 45,
        "cherry": 1000
    }
}

@app.route('/stock')
def get_stock():
    return jsonify(stock)

@app.route("/stock/<collection>")
def get_collection(collection):
    """ Returns a collection from stock """
    if collection in stock:
        return jsonify(stock[collection])
    return jsonify({"error": "Not found"}), 404

@app.route("/stock/<collection>/<member>")
def get_member(collection, member):
    """ Returns the qty of the collection member """
    if collection in stock:
        member = stock[collection].get(member)
        if member:
            return jsonify(member)
        return jsonify({"error": "Not found"}), 404
    return jsonify({"error": "Not found"}), 404

# Step 4 - Processing Incoming Data: https://www.digitalocean.com/community/tutorials/processing-incoming-request-data-in-flask#using-json-data
@app.route("/stock/<collection>", methods=["POST"])
def post_collection(collection):
    """ Handles the posted JSON data from the HTTP Body"""
    # request.is_json returns True if the request body is JSON
    if request.is_json and collection in request.get_json().keys():
        # request.get_json returns a dictionary
        json_data = request.get_json()  # alternative: json_data = request.json
            
        # insert new data in stock, if not exists --> else conflict 409
        if not collection in stock.keys():
            stock[collection] = json_data[collection]
            return jsonify(json_data), 201
        else:
            return jsonify({"error": "Conflict"}), 409
    else:
        return jsonify({"error": "Bad request"}), 400


