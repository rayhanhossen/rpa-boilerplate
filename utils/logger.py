import logging
import traceback
from datetime import datetime
from utils.config import ConfigParser

# class instance
config = ConfigParser().get_config()


class Logger:
    INFO = 'INFO'
    DEBUG = 'DEBUG'
    production = 'production'
    development = 'development'
    __instance = None

    def __init__(self, project_name='RPA Framework',
                 filename=f'{config.get("log_dir_path")}/app_{datetime.now().strftime("%d_%m_%Y")}.log',
                 loglevel=INFO, mode=production):
        self.logger = logging.getLogger(__name__)
        if mode == self.development:
            if loglevel == self.INFO:
                logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
            else:
                logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                                    level=logging.DEBUG)
        else:
            if loglevel == self.INFO:
                logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO,
                                    filename=filename, filemode='a')
            else:
                logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                                    level=logging.DEBUG,
                                    filename=filename, filemode='a')
        self._project_name = project_name

    @staticmethod
    def get_instance():
        """ Static access method. """
        if Logger.__instance is None:
            Logger.__instance = Logger(loglevel=Logger.DEBUG)
        return Logger.__instance

    def log_start(self):
        self.logger.info('-------Starting Logging--------')
        self.logger.info(self._project_name)

    def log_error(self, exception):
        self.logger.error(traceback.format_exc())
        self.logger.warning(exception)

    def log_error_msg(self, msg):
        self.logger.error(msg)

    def log_end(self):
        self.logger.info('-------Ending Logging----------')
        self.logger.info(self._project_name)

    def log_info(self, msg):
        self.logger.info(msg=msg)

    def log_debug(self, msg):
        msg = f"\n{msg}"
        self.logger.debug(msg=msg)

    def log_warn(self, msg):
        self.logger.warning(msg=msg)

    def log_critical(self, msg):
        self.logger.critical(msg=msg)
