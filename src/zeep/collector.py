"""
Generic collector code to run config file
"""
from __future__ import print_function

from inputs.serial_connector import SerialSensor
from connectors import (dweet, file_system, io_adafruit, influx)
from settings import SERVICES
from time import sleep
import logging
import argparse
import sys


LOGGING_LEVEL = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warn': logging.WARN,
    'error': logging.ERROR
}


def run():
    parser = argparse.ArgumentParser(
        description='Update services with output from serial monitor.')
    parser.add_argument('-d', '--device',
                        metavar='DEVICE',
                        help='Device in /dev attached to the ' +
                        'serial device e.g. ttyUSB0')
    parser.add_argument('-l', '--log-level', default='info',
                        help='Set the log level')

    args = parser.parse_args()

    logger = logging.getLogger(__file__)
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.setLevel(LOGGING_LEVEL[args.log_level])

    logger.info("Starting reading from serial...")

    logger.debug("Connecting to /dev/{}".format(args.device))

    sensor_reader = SerialSensor(port=args.device, logger=logger)

    while(True):

        reading = sensor_reader.read()

        logger.debug("Reading: {}".format(reading))

        for name, setting in SERVICES.items():
            if name == 'DWEET_NAME':
                conn = dweet.DweetConnector(setting)
            elif name == 'ADAFRUITIO_KEY':
                conn = io_adafruit.IOAdafruitConnector(setting)
            elif name == 'FILE_SYSTEM_PATH':
                conn = file_system.FileSystemConnector(setting)
            elif name == 'INFLUXDB':
                conn = influx.InfluxDBConnector(logger, setting)
            conn.send(reading)
        sleep(10)


if __name__ == "__main__":
    run()
