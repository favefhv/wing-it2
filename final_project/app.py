from flask import Flask, jsonify, render_template, request
from flasgger import Swagger
from Api import Api
from Views import Views

app = Flask(__name__)
app.config['SWAGGER'] = {
    'title': 'WING Sensor API'
}
swagger = Swagger(app)

# path for files (storage - see c:/tmp) 
path_to_data = "/tmp/"

api = Api(path_to_data)
views = Views(path_to_data)

# --------------- Frontend ---------------
@app.route('/')
def index():
    return render_template('index.html')

@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', error = error), 404

@app.route('/sensors')
def get_sensors():
    return render_template('sensors.html', sensors=views.get_sensors())

@app.route('/sensors/<int:sensor_id>')
def get_sensor_data(sensor_id):
    return render_template('sensor.html', sensor_data=views.get_sensor_data(sensor_id), sensor = sensor_id)

# --------------- API ---------------
@app.route('/api/sensors', methods=['GET'])
def sensors():
    """This method returns the IDs of the existing sensors
    ---
    responses:
      200:
        description: A list of sensor IDs
        schema:
          type: array
          items:
              type: string
    """
    return jsonify(api.get_sensors()), 200

@app.route('/api/sensors/<int:sensor_id>', methods=['POST'])
def add_sensor_data(sensor_id):
    """This method adds new sensor data. If the sensor does not exist, it will be created.
    ---
    parameters:
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
    return jsonify(api.add_sensor_data(sensor_id, request.json["value"])), 201

@app.route('/api/generate_data')
def generate_data():
    """Generate sample sensor data
    ---
    responses:
      201:
        description: OK if sensor data was created
        schema:
          type: object
          additionalProperties:
            $ref: '#/definitions/SensorData'
    """
    return jsonify(api.generate_test_data()), 201

@app.route('/api/sensors', methods=['DELETE'])
def sensors_delete():
    """This method deletes all sensors with its data
    ---
    responses:
      204:
        description: Successfully deleted sensors
    """
    return jsonify(api.delete_sensors()), 204