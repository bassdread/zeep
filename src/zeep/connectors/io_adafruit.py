from Adafruit_IO import Client

try:
    from settings import SERVICES
except ImportError:
    # service not configured
    pass


class IOAdafruitConnector(object):

    def __init__(self, api_key=None):

        if not api_key:
            api_key =  SERVICES['ADAFRUITIO_KEY']

        self.aio = Client(api_key)

    def send(self, data):
        # send data to dweet

        try:
            for key, value in data.iteritems():
                self.aio.send(key, value)

            response = {'status': 'ok'}
        except Exception as exception:
            response = {'error': exception.message}

        return response
