"""
Generic collector code to run config file
"""

from inputs.serial_connector import SerialSensor
from connectors import dweet
from settings import *

SERVICES_TO_UPDATE = [
    'dweet',
    'io_adafruit',
    'filesystem'
]

def run():
    print "running"
    sensor_reader = SerialSensor()

    reading = sensor_reader.read()

    print reading

    for service in SERVICES_TO_UPDATE:
        if service == 'dweet':
            dweet_conn = dweet.DweetConnector()

if __name__ == "__main__":
    run()
