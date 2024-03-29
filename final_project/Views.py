from datetime import datetime
import os
import json

class Views:
    def __init__(self, path_to_data):
        self.__path_to_data = path_to_data

    def __date_hook(self, json_dict):
        """Converts string date/time values to date time object"""
        for (key, value) in json_dict.items():
            try:
                json_dict[key] = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
            except Exception as ex:
                pass
        return json_dict

    # def get_sensors(self):
    #     """Retrieves a list of all sensors for a customer."""
    #     sensors = []
    #     if os.path.exists(self.__path_to_data):
    #         with os.scandir(self.__path_to_data) as entries:
    #             for entry in entries:
    #                 sensors.append(entry.name[:-4])
    #     return sensors

    def get_sensors(self):
        """Retrieves a list of all sensors for a customer with current state of sensor."""
        sensors = []
        if os.path.exists(self.__path_to_data):
            with os.scandir(self.__path_to_data) as entries:
                for entry in entries:
                    with open(self.__path_to_data + "/" + entry.name, "r") as f:
                        sensor_data = f.readlines()
                    sensors.append({ "name" : entry.name[:-4], "status" : json.loads(sensor_data[-1], object_hook=self.__date_hook)["value"] })
        return sensors

    def get_sensor_data(self, sensor_id):
        """Retrievs sensor data for a specific sensor for a customer."""
        sensor_data = []
        if os.path.exists(self.__path_to_data + "/" + str(sensor_id) + ".txt"):
            with open(self.__path_to_data + "/" + str(sensor_id) + ".txt", "r") as f:
                data = f.readlines()
            for line in data:
                # siehe dazu: https://stackoverflow.com/questions/8793448/how-to-convert-to-a-python-datetime-object-with-json-loads - json.loads(dumped_dict, object_hook=date_hook)
                sensor_data.append(json.loads(line, object_hook=self.__date_hook))
            return sensor_data
        else:
            raise Exception("Data for sensor ID " + sensor_id + " not found.")