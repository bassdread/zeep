import dweepy
from settings import DWEET_NAME

class DweetConnector(object):

    def __init__(self, dweet_name=None):

        if not dweet_name:
            dweet_name = DWEET_NAME

        self.dweet_name = dweet_name

    def send(self, data):
        # send data to dweet

        try:
            response = dweepy.dweet_for(self.dweet_name, data)
        except Exception as exception:
            response = {'error': exception.message}

        return response