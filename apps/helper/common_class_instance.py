from utils.logger import Logger

from utils.config import ConfigParser


class CommonClassInstance:
    __instance = None

    def __init__(self):
        self.logger = Logger.get_instance()
        self.config = ConfigParser().get_config()

    @staticmethod
    def get_instance():
        """ Static access method. """
        if CommonClassInstance.__instance is None:
            CommonClassInstance.__instance = CommonClassInstance()
        return CommonClassInstance.__instance
