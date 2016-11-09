"""
Generic collector code to run config file
"""

from inputs.serial_connector import SerialSensor
from connectors import (dweet, file_system, io_adafruit, influx)
from settings import SERVICES
from time import sleep


def run():
    sensor_reader = SerialSensor()

    reading = sensor_reader.read()

    for name, setting in SERVICES.iteritems():
        if name == 'DWEET_NAME':
            conn = dweet.DweetConnector(setting)
        elif name == 'ADAFRUITIO_KEY':
            conn = io_adafruit.IOAdafruitConnector(setting)
        elif name == 'FILE_SYSTEM_PATH':
            conn = file_system.FileSystemConnector(setting)
        elif name == 'INFLUXDB':
            conn = influx.InfluxDBConnector(setting)

        conn.send(reading)

if __name__ == "__main__":
    run()
