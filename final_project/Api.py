from datetime import datetime, timedelta
import random
import shutil
import os
import json

class Api:
    def __init__(self, path_to_data):
        self.__path_to_data = path_to_data

    def get_sensors(self):
        """Retrieves a list of all sensor IDs."""
        sensors = []
        if os.path.exists(self.__path_to_data):
            with os.scandir(self.__path_to_data) as entries:
                for entry in entries:
                    sensors.append(entry.name[0:entry.name.find(".")])
        
        return sensors
    
    def delete_sensors(self):
        """Deletes all sensors and its data."""
        if os.path.exists(self.__path_to_data):
            shutil.rmtree(self.__path_to_data)

    def add_sensor_data(self, sensor_id, value):
        """Adds a new sensor record to the storage"""
        if os.path.exists(self.__path_to_data):
            data = { "datetime" : datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "value" : value }
            with open(self.__path_to_data + "/" + str(sensor_id)+".txt", "a+") as f:
                f.write(json.dumps(data) + "\n")
                return data
        else:
            raise Exception("Data for sensor ID " + sensor_id + " not found.")

    def generate_test_data(self):
        """Generate test data for demo purposes"""
        no_sensors = 5
        no_on_of_pairs_per_sensor = 2
        sensor_data = {}

        # remove existing folder
        self.delete_sensors()
        # create root folder        
        os.makedirs(self.__path_to_data)    
        
        # generate random data
        for sensor_id in range(1, no_sensors + 1):
            with open(self.__path_to_data + "/" + str(sensor_id)+".txt", "w") as f:
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