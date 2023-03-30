import ssl
import urllib

from logger import Logger

from module.config.config import ConfigParser

# instance of other class
logger = Logger.get_instance()
config = ConfigParser().get_config()


class SmsAPI:
    def __init__(self):
        self.sms_api_url = config.sms_api_url
        self.username = config.sms_api_username
        self.password = config.sms_api_password

    def send(self, msisdn, msg):
        try:
            ssl._create_default_https_context = ssl._create_unverified_context
            msg = urllib.parse.quote_plus(msg, encoding='UTF-8')
            final_url = f"{self.sms_api_url}?user=CallDropMin&password=C@11Dr0pM!n&src=Robi%20Rebate&dst={msisdn}&msg={msg}&dr=1&type=u"
            resource = urllib.request.urlopen(final_url)
            response = resource.read()
            response = str(response)
            response = response.strip("b'")
            print(f'Response - {response}')
            logger.log_info(f'Response - {response}')
        except Exception as e:
            logger.log_error(exception=e)