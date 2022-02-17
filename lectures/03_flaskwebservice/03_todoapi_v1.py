from flask import Flask, jsonify
app = Flask(__name__)

todoes = [{"id":1,
      "title":"Get used to HTTP Requests",
      "description":"Send Get, Post, Put and Delete Request to REST API.",
      "completed":False,
      "targetDate":"2022-02-26"}]

@app.route('/api/todoes/')
def index():
    """returns all todoes"""
    return jsonify(todoes), 200

@app.route('/api/todoes/<int:id>', methods=['GET'])
def getById(id):
    """return todo by id"""
    for todo in todoes:
        if todo["id"] == id:
            return jsonify(todo), 200
    return jsonify({"error": "Not found"}), 404

def getMaxID():
    maxId = 0;
    for todo in todoes:
        if todo["id"] > maxId:
            maxId = todo["id"]
    return maxId + 1

from flask import request
from datetime import date

@app.route("/api/todoes/", methods=["POST"])
def postToDo():
    """creates a todo item"""
    if request.is_json:
        json_data = request.get_json()
        
        # https://thispointer.com/python-how-to-check-if-a-key-exists-in-dictionary/
        if json_data.get("id") is None and json_data.get("title") is not None and json_data.get("description") is not None:
            json_data["id"] = getMaxID()
            if json_data.get("completed") is None:
                json_data["completed"] = False
            if json_data.get("targetDate") is None:
                json_data["targetDate"] = date.today().strftime('%Y-%m-%d')
            todoes.append(json_data)
            return jsonify(json_data), 201
    return jsonify({"error": "Bad request"}), 400
    
@app.route("/api/todoes/<int:id>", methods=["PUT"])
def putToDo(id):
    """updates a todo item"""
    selTodo = None
    for todo in todoes:
        if todo["id"] == id:
            selTodo = todo
            break
    if not selTodo:
        return jsonify({"error": "Not Found"}), 404
    
    if request.is_json and request.get_json().get("id") is not None:
        json_data = request.get_json()
        
        if selTodo["id"] == json_data["id"]:
            if json_data.get("title") is not None:
                selTodo["title"] = json_data["title"]
            if json_data.get("description") is not None:
                selTodo["description"] = json_data["description"]
            if json_data.get("completed") is not None:
                selTodo["completed"] = json_data["completed"]
            if json_data.get("targetDate") is not None:
                selTodo["targetDate"] = json_data["targetDate"]
            return jsonify(selTodo), 200
        else:
            return jsonify({"error": "Conflict"}), 409
    else:
        return jsonify({"error": "Bad request"}), 400

@app.route('/api/todoes/<int:id>', methods=['DELETE'])
def deleteToDo(id):
    """deletes a todo item"""
    for todo in todoes:
        if todo["id"] == id:
            todoes.remove(todo)
            return {}, 204
    return jsonify({"error": "Not found"}), 404

