from flask import Flask, jsonify
from flasgger import Swagger   #  install the module for vs code: py -m pip install flasgger
app = Flask(__name__)
app.config['SWAGGER'] = { 'title' : 'WING ToDoes API' }
swagger = Swagger(app)

todoes = [{"id":1,
      "title":"Get used to HTTP Requests",
      "description":"Send Get, Post, Put and Delete Request to REST API.",
      "completed":False,
      "targetDate":"2022-02-26"}]

@app.route('/api/todoes/')
def index():
    """ Returns all todoes
    ---
    definitions:
      ToDoes:
        type: array
        items:
          $ref: '#/definitions/ToDo'
      ToDo:
        type: object
        properties:
          id: 
            type: integer
          title:
            type: string
          description:
            type: string
          completed:
            type: boolean
          targetDate:
            type: string
            description: target date
            example: "2021-01-01"
            format: date
            pattern: "YYYY-MM-DD"
            minLength: 0
            maxLength: 10
    responses:
      200:
        description: A list of todoes
        schema:
          $ref: '#/definitions/ToDoes'
    """  
    return jsonify(todoes), 200

@app.route('/api/todoes/<int:id>', methods=['GET'])
def getById(id):
    """ Returns a todo by id
    ---
    ---
    parameters:
      - name: id
        in: path
        type: integer
        default: 0
        required: true
    responses:
      200:
        description: A todo
        schema:
          $ref: '#/definitions/ToDo'
    """  
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
    """This method adds new todo
    ---
    parameters:
      - name: body
        in: body
        required: true
        example: {'title':'Title of ToDo','description':'Description of ToDo','completed':False,'targetDate':'2022-02-26'}
    responses:
      201:
        description: Adds a todo
        schema:
          $ref: '#/definitions/ToDo'
    """
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
    """This method updates an existing todo
    ---
    parameters:
      - name: id
        in: path
        type: integer
        default: 0
        required: true
      - name: body
        in: body
        required: true
        example: {'id':0,'title':'Title of ToDo','description':'Description of ToDo','completed':False,'targetDate':'2022-02-26'}
    responses:
      200:
        description: Updates a todo
        schema:
          $ref: '#/definitions/ToDo'
    """
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
    """This method deletes a todo
    ---
    ---
    parameters:
      - name: id
        in: path
        type: integer
        default: 0
        required: true
    responses:
      204:
        description: No Content
    """  
    for todo in todoes:
        if todo["id"] == id:
            todoes.remove(todo)
            return {}, 204
    return jsonify({"error": "Not found"}), 404