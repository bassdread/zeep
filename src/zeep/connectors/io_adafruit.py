from Adafruit_IO import Client


class IOAdafruitConnector(object):

    def __init__(self, api_key):

        self.aio = Client(api_key)

    def send(self, data):
        # send data to dweet

        try:
            for key, value in data.iteritems():
                aio.send(key, value)
        except Exception as exception:
            response = {'error': exception.message}

        return response