from flask import Flask, Response, render_template, request
from flasgger import Swagger
from Api import Api
from Views import Views
from Security import Security
import json

app = Flask(__name__)
app.config['SWAGGER'] = {
    'title': 'WING Sensor API'
}
swagger = Swagger(app)

path_to_data = "/tmp/"

security = Security(path_to_data)
api = Api(path_to_data, security)
views = Views(path_to_data, security)

# --------------- Frontend ---------------
@app.route('/')
def index():
    return render_template('index.html')

@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', error = error), 404

@app.route('/sensors/<api_key>')
def get_sensors(api_key):
    return render_template('sensors.html', sensors=views.get_sensors(api_key), api_key = api_key)

@app.route('/sensors/<api_key>/<int:sensor_id>')
def get_sensor_data(api_key, sensor_id):
    return render_template('sensor.html', sensor_data=views.get_sensor_data(api_key, sensor_id), sensor = sensor_id)

# --------------- API ---------------
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
    responses:
      200:
        description: A list of sensor IDs
        schema:
          type: array
          items:
              type: string
    """
    return Response(json.dumps(api.get_sensors(api_key = request.headers.get("api_key"))), status=200, mimetype='application/json')

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
    definitions:
      SensorData:
        type: object
        properties:
          datetime:
            type: string
          value:
            type: boolean
    responses:
      201:
        description: The added sensor data
        schema:
          $ref: '#/definitions/SensorData'
    """
    return Response(json.dumps(api.add_sensor_data(request.headers.get("api_key"), sensor_id, json.loads(request.data)["value"])), status=201, mimetype='application/json')

@app.route('/api/generate_key')
def generate_key():
    """This method returns a new API key
    ---
    responses:
      201:
        description: newly generated API key
        schema:
          type: string
    """
    return api.generate_new_api_key(), 201

@app.route('/api/generate_data')
def generate_data():
    """Generate test sensor data
    ---
    responses:
      201:
        description: OK if sensor data was created
        schema:
          type: object
          additionalProperties:
            $ref: '#/definitions/SensorData'
    """
    return Response(json.dumps(api.generate_test_data()), status=201, mimetype='application/json')
