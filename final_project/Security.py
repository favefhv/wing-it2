import os

class Security:
    def __init__(self, path_to_data):
        self.__path_to_data = path_to_data

    def is_key_valid(self, api_key):
        """Checks if the given API key is valid"""
        return os.path.exists(self.__path_to_data + api_key)