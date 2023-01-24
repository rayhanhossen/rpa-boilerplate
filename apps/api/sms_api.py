class SmsAPI:
    def __init__(self, sms_api_url, username, password):
        self.sms_api_url = sms_api_url
        self.username = username
        self.password = password

    def send(self, msisdn, msg):
        pass
