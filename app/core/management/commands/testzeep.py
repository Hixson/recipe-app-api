import requests
import zeep


class ServiceNow:

    def __init__(self, instance, username, password):
        self.instance = instance
        self.session = requests.Session()
        self.session.auth = requests.auth.HTTPBasicAuth(username, password)
        self.transport = zeep.transports.Transport(session=self.session)

    def client(self, tablename):
        wsdl_url = 'https://%s.service-now.com/%s.do?WSDL' % (
            self.instance, tablename)
        print(wsdl_url)
        return zeep.CachingClient(wsdl_url, transport=self.transport)
