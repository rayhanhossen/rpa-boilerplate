import json


class ConfigParser:

    def __init__(self):
        with open("../env_config.json", encoding="utf-8") as config_file:
            conf = json.load(config_file)
        self.conf = conf

    def get_config(self):
        return self.conf
