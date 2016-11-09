#!/usr/bin/python

import collections
from datetime import datetime
import json
import sensors
from traceback import print_exc

IGNORE_READINGS = ['fan0', 'fan1', 'fan3', 'fan4', 'fan5', 'cpu_fan']
DATA_FILE_LOCATION = '/tmp/sensors_output.json'

USE_INFLUX = True
USE_REDIS = False


def fetch_sensor_data():

    try:
        sensors.init()
        data = {}

        for chip in sensors.iter_detected_chips():
            for feature in chip:
                # log stuff we care about
                if feature.label not in IGNORE_READINGS:
                    data[feature.label] = round(feature.get_value(), 3)

        sorted_data = collections.OrderedDict(sorted(data.items()))

        write_data_file(sorted_data)

        if USE_REDIS:
            import redis
            REDIS_CONNECTION = redis.StrictRedis(host='localhost', port=6379, db=0)
            write_data_redis(sorted_data)

        if USE_INFLUX:
            from influxdb import InfluxDBClient
            INFLUX_CLIENT = InfluxDBClient('localhost', 8086, 'root', 'root', 'jarvis')
            write_data_influx(sorted_data, INFLUX_CLIENT)

        for name, reading in sorted_data.iteritems():
            print "{0}: {1}".format(name, reading)

    except Exception as exception:
        print_exc()
        print "Failed to get sensor data: {0}".format(exception.message)


def write_data_influx(data, INFLUX_CLIENT):
    json_payload = []
    time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    try:
        for name, value in data.iteritems():
            payload = {
                "measurement": name,
                "tags": {
                    "host": "jarvis",
                    "location": "garage"
                },
                "time": time,
                "fields": {
                    "value": value
                }
            }
            json_payload.append(payload)
        INFLUX_CLIENT.write_points(json_payload)
    except Exception as exception:
        print_exc()
        print "Failed to write to Influx. Error {}".format(exception.message)


def write_data_redis(data):
    try:
        for name, value in data.iteritems():
            REDIS_CONNECTION.set(name, value)
    except Exception as exception:
        print_exc()
        print "Failed to write to Redis. Error {}".format(exception.message)


def write_data_file(data):
    try:
        data['time'] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        with open(DATA_FILE_LOCATION, 'w') as data_file:
            data_file.write(json.dumps(data))
            data_file.close()

        return True
    except Exception as exception:
        print_exc()
        print "Failed to write to data file. Error {}".format(
            exception.message)


if __name__ == "__main__":
    fetch_sensor_data()
