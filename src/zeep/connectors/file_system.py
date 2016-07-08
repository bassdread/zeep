""" Simple class to write json out to a file
"""
import json


class FileSystemConnector(object):

    def __init__(self, file_name):
        self.file_name = file_name

    def send(self, data):

        try:
            f = open(self.file_name, 'w')
            f.write(json.dumps(data))
            f.close()

        except Exception as exception:
            response = {'error': exception.message}

        return response