import json
import sys

from modules.encryption.crypto_pass_phase import CryptoPassPhase


class ConfigParser:

    def __init__(self):
        with open("../env_config.json", encoding="utf-8") as config_file:
            conf = json.load(config_file)
        self.conf = conf

    @staticmethod
    def stop_execution():
        print('Stopping Execution')
        sys.exit('Stopping Execution')

    def encrypt_key(self, key):
        pass_phase = self.conf['PassPhase']
        encrypted = CryptoPassPhase.encrypt(pass_phase, key)
        print(encrypted)
        self.stop_execution()

    def get_config(self):
        return self.conf
