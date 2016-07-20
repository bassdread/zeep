""" Simple class to write json out to a file
"""
import json
from settings import SERVICES


class FileSystemConnector(object):

    def __init__(self, file_name=None):

        if not file_name:
            file_name =  SERVICES['FILE_SYSTEM_PATH']

        self.file_name = file_name

    def send(self, data):

        try:
            f = open(self.file_name, 'w')
            f.write(json.dumps(data))
            f.close()
            response = {'status': 'ok'}

        except Exception as exception:
            response = {'error': exception.message}

        return response
