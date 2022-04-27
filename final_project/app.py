from flask import Flask
from flasgger import Swagger

app = Flask(__name__)
app.config['SWAGGER'] = {
    'title': 'WING Sensor API'
}
swagger = Swagger(app)

import os
path_to_data = "/tmp/"

def check_valid_key(api_key):
    if not os.path.exists(path_to_data + api_key):
        raise Unauthorized()

@app.route('/')
def index():
    return render_template('index.html')

@app.errorhandler(404)
def not_found(error):
    return render_template('error.html'), 404

# from flask import render_template
# from werkzeug.exceptions import Unauthorized, NotFound
# @app.route('/sensors/<api_key>')
# def get_sensors(api_key):
#     check_valid_key(api_key)
#     sensors = []
#     with os.scandir(path_to_data + api_key) as entries:
#         for entry in entries:
#             sensors.append(entry.name[:-4])
#     return render_template('sensors.html', sensors=sensors, api_key = api_key)

from flask import render_template
from werkzeug.exceptions import Unauthorized, NotFound
@app.route('/sensors/<api_key>')
def get_sensors(api_key):
    check_valid_key(api_key)
    sensors = [ ]
    with os.scandir(path_to_data + api_key) as entries:
        for entry in entries:
            with open(path_to_data + api_key + "/" + entry.name, "r") as f:
                sensor_data = f.readlines()
            sensors.append({ "name" : entry.name[:-4], "status" : json.loads(sensor_data[-1], object_hook=date_hook)["value"] })
    return render_template('sensors.html', sensors=sensors, api_key = api_key)

def date_hook(json_dict):
    for (key, value) in json_dict.items():
        try:
            json_dict[key] = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
        except Exception as ex:
            pass
    return json_dict

@app.route('/sensors/<api_key>/<int:sensor_id>')
def get_sensor_data(api_key, sensor_id):
    check_valid_key(api_key)
    sensor_data = []
    if os.path.exists(path_to_data + api_key + "/" + str(sensor_id) + ".txt"):
        with open(path_to_data + api_key + "/" + str(sensor_id) + ".txt", "r") as f:
            data = f.readlines()
        for line in data:
            # siehe dazu: https://stackoverflow.com/questions/8793448/how-to-convert-to-a-python-datetime-object-with-json-loads - json.loads(dumped_dict, object_hook=date_hook)
            sensor_data.append(json.loads(line, object_hook=date_hook))  
        return render_template('sensor.html', sensor_data=sensor_data, sensor = sensor_id)
    else:
        raise NotFound()

from flask import request
import json
#Step 5 - generate json: 
@app.route('/api/sensors', methods=['GET'])
def sensors():
    """This method returns the existing sensors based on your api_key
    ---
    parameters:
      - name: api_key
        in: header
        type: string
        required: true
        default: wing_test
    definitions:
      Sensor:
        type: array
        items:
            type: integer
    responses:
      200:
        description: A list of sensors
        schema:
          $ref: '#/definitions/Sensor'
    """
    api_key = request.headers.get("api_key")
    check_valid_key(api_key)
    sensors = []
    with os.scandir(path_to_data + api_key) as entries:
        for entry in entries:
            sensors.append(entry.name[0:entry.name.find(".")])
    return Response(json.dumps(sensors), status=200, mimetype='application/json')

from flask import Response
from datetime import datetime, timedelta
@app.route('/api/sensors/<int:sensor_id>', methods=['POST'])
def add_sensor_data(sensor_id):
    """This method adds new sensor data
    ---
    parameters:
      - name: api_key
        in: header
        type: string
        required: true
        default: wing_test
      - name: sensor_id
        in: path
        type: integer
        default: 0
        required: true
      - name: body
        in: body
        required: true
        example: {'value': true}
    responses:
      201:
        description: Adds a value to a sensor
        schema:
          $ref: '#/definitions/Sensor'
    """
    api_key = request.headers.get("api_key")
    check_valid_key(api_key)
    if os.path.exists(path_to_data + api_key):
        data = { "datetime" : datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "value" : json.loads(request.data)["value"] }
        with open(path_to_data + api_key + "/" + str(sensor_id)+".txt", "a+") as f:
            f.write(json.dumps(data) + "\n")
        return Response(json.dumps(data), status=201, mimetype='application/json')
    else:
        raise NotFound()

import secrets
@app.route('/api/generate_key')
def generate_key():
    """This method returns a new API key
    ---
    responses:
      200:
        description: newly generated API key
        schema:
          type: string
    """
    generated_key = secrets.token_urlsafe(8)
    os.makedirs(path_to_data + generated_key)
    return generated_key

import random

@app.route('/api/generate_data')
def generate_data():
    """Generate test sensor data
    ---
    responses:
      200:
        description: OK if sensor data was created
    """
    api_key = "wing_test"
    if not os.path.exists(path_to_data + api_key):
        os.makedirs(path_to_data + api_key)
    for sensor_id in range(5):
        for i in range(3):
            data = { "datetime" : (datetime.now() + timedelta(seconds=i)).strftime("%Y-%m-%d %H:%M:%S"), "value" : bool(random.randint(0, 1)) }
            with open(path_to_data + api_key + "/" + str(sensor_id)+".txt", "a+") as f:
                f.write(json.dumps(data) + "\n")
    return Response(json.dumps(data), status=201, mimetype='application/json')
