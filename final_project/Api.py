from datetime import datetime, timedelta
import random
import shutil
import os
import json
import secrets

class Api:
    def __init__(self, path_to_data, security):
        self.__path_to_data = path_to_data
        self.__security = security

    def get_sensors(self, api_key):
        """Retrieves a list of all sensor IDs for a customer."""
        self.__security.is_key_valid(api_key) # TODO was tun, wenn key nicht valid ist - mit if-else abfragen oder raise Exception?
        
        sensors = []
        with os.scandir(self.__path_to_data + api_key) as entries:
            for entry in entries:
                sensors.append(entry.name[0:entry.name.find(".")])
        
        return sensors

    def add_sensor_data(self, api_key, sensor_id, value):
        """Adds a new sensor record to the storage"""
        self.__security.is_key_valid(api_key) # TODO was tun, wenn key nicht valid ist - mit if-else abfragen oder raise Exception?
        if os.path.exists(self.__path_to_data + api_key):
            data = { "datetime" : datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "value" : value }
            with open(self.__path_to_data + api_key + "/" + str(sensor_id)+".txt", "a+") as f:
                f.write(json.dumps(data) + "\n")
                return data
        else:
            raise Exception("Data for sensor ID " + sensor_id + " not found.")

    def generate_new_api_key(self):
        """Generate a key for a new customer"""
        generated_key = secrets.token_urlsafe(8)
        os.makedirs(self.__path_to_data + generated_key)
        return generated_key

    def generate_test_data(self):
        """Generate test data for demo purposes"""
        api_key = "wing_test"
        no_sensors = 5
        no_on_of_pairs_per_sensor = 2
        sensor_data = {}

        # remove existing folder
        if os.path.exists(self.__path_to_data + api_key):
            shutil.rmtree(self.__path_to_data + api_key)
        
        os.makedirs(self.__path_to_data + api_key)    
        
        # generate random data
        for sensor_id in range(1, no_sensors + 1):
            with open(self.__path_to_data + api_key + "/" + str(sensor_id)+".txt", "w") as f:
                for i in range(no_on_of_pairs_per_sensor * 2): # 2 --> on + off state
                    data = { "datetime" : (datetime.now() + timedelta(minutes=i)).strftime("%Y-%m-%d %H:%M:%S"), "value" : False if i % 2 == 0 else True }
                    f.write(json.dumps(data) + "\n")

                    if not sensor_id in sensor_data.keys():
                        sensor_data[sensor_id] = []

                    sensor_data[sensor_id].append(data)
                
                # randomly switch off lights
                if random.randint(0, 1) == 0:
                    data = { "datetime" : (datetime.now() + timedelta(minutes=i)).strftime("%Y-%m-%d %H:%M:%S"), "value" : False }
                    f.write(json.dumps(data) + "\n")
        return sensor_data