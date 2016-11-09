from influxdb import InfluxDBClient
import json
from datetime import datetime


try:
    from settings import SERVICES
except ImportError:
    # service not configured
    pass


class InfluxDBConnector(object):


    def __init__(self, database_name=None):

        if not database_name:
            database_name = services['INFLUXDB']

        self.database_name = database_name
        self.influx_client = InfluxDBClient('localhost', 8086, 'root', 'root', self.database_name)

    def send(self, data):

        if not data:
            f = open('/tmp/zeep_latest_reading.json', 'r')
            data = f.read()
            data = json.loads(data)
            f.close()

        json_payload = []
        time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        try:
            for name, value in data.iteritems():
                payload = {
                    "measurement": name,
                    "tags": {
                        "host": "jarvis",
                        "location": "office"
                    },
                    "time": time,
                    "fields": {
                        "value": value
                    }
                }
                json_payload.append(payload)
            self.influx_client.write_points(json_payload)
        except Exception as exception:
            print_exc()
            print "Failed to write to Influx. Error {}".format(exception.message)
