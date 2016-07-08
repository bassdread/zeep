"""Read data from serial port.
By default we assume the data coming over the serial port
is JSON.

This can be changed to expect csv by:

sensor = SerialSensor(port='ttyUSB0', json_data=False)

"""

import glob
import json
import serial
import os.path
import time

# usual linux ports
PORTS = ['ttyUSB0', 'ttyAMA0', 'ttyACM0']
OSX_PORTS = ['tty.usbserial-*']
SERIAL_PORT_PATH_ROOT = '/dev/'


class SerialSensor():

    def __init__(self, port=None, json_data=True, debug=False):
        if port:
            self.serial_port = SERIAL_PORT_PATH_ROOT + port
        else:
            self.serial_port = self._detect_port()
        self.ser = serial.Serial(self.serial_port, 9600, timeout=1)

        self.debug = debug
        self.json_data = json_data

        if self.debug:
            print "Using {} as serial port".format(self.serial_port)

    def read(self, timeout=10):

        if not self.serial_port:
            print "Unable to find anything on the serial port to read from."
            return

        stop = time.time() + timeout
        i = 0

        while time.time() < stop:
            i = i + 1
            raw_serial = self.ser.readline()
            if self.debug:
                print "Attempt {0}: Received: {1}".format(i, raw_serial)

            if self.json_data and raw_serial:
                try:
                    return json.loads(raw_serial)
                except Exception as exception:
                    if self.debug:
                        print "Failed to decode to JSON: {0}".format(
                            raw_serial)
                        print exception.message
            elif raw_serial:
                try:
                    raw_serial = raw_serial.replace('\r\n', '')
                    return raw_serial.split(',')
                except:
                    # keep going we might get lucky
                    pass
            else:
                if self.debug:
                    print "Failed to decode anything"

    def _detect_port(self):

        device_path = None

        for port in PORTS:
            device = SERIAL_PORT_PATH_ROOT + port
            if os.path.exists(device):
                device_path = device

        if not device_path:
            # lets try osx stuff
            for file_name in glob.glob1("/dev", "tty.usbserial-*"):
                device_path = SERIAL_PORT_PATH_ROOT + file_name
        return device_path
