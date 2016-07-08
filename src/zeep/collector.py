"""
Generic collector code to run config file
"""

from inputs.serial_connector import SerialSensor
from connectors import (dweet, file_system, io_adafruit)
from settings import *
from time import sleep


SERVICES_TO_UPDATE = [
    'dweet',
    'io_adafruit',
    'file_system'
]

def run():
    print "running"

    while(True):
        sensor_reader = SerialSensor()

        reading = sensor_reader.read()

        print reading

        for service in SERVICES_TO_UPDATE:
            if service == 'dweet':
                conn = dweet.DweetConnector()
            elif service == 'io_adafruit':
                conn = io_adafruit.IOAdafruitConnector()
            elif service == 'file_system':
                conn = file_system.FileSystemConnector()

            conn.send(reading)

        sleep(30)

if __name__ == "__main__":
    run()
