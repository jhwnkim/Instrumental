# -*- coding: utf-8  -*-
"""
Driver for DiCon FiberOptics MEMS 1xN Optical Switch Module on RS232 communication

Usage Example:
from instrumental.drivers.opticalswitch.diconopticalswitch import DiConOpticalSwitch
switch = DiConOpticalSwitch(port='COM7')
switch.identify()
switch.close()
"""

from . import OpticalSwitch
from serial import Serial
import re

class DiConOpticalSwitch(OpticalSwitch):
    _INST_PARAMS_ = ['port']

    def _initialize(self):
        self._ser = Serial(self._paramset['port'], baudrate=115200, timeout=1.0)
        self._channel = 0

        # Read number of channels from module
        self._ser.reset_input_buffer()
        self._ser.write(b'CF?\r')
        self._ser.read() # dummy read the newline
        self._channel_max = int(re.split(',', self._ser.readline())[1])
        # self._channel_max = 16

    def identify(self):
        self._ser.reset_input_buffer()
        self._ser.write(b'ID?\r')
        self._ser.read() # dummy read the newline
        print(self._ser.readline())

    def set_channel(self, new_channel):
        if new_channel >=0 and new_channel <= self._channel_max:
            self._channel = new_channel
            self._ser.reset_input_buffer()
            self._ser.write(bytes('I1 {}\r'.format(new_channel), 'utf-8'))
        else:
            print('DiConOpticalSwitch: Invalid channel')

    def get_channel(self):
        self._ser.reset_input_buffer()
        self._ser.write(b'I1?\r')
        self._ser.read() # dummy read the newline
        print(self._ser.readline())

    def close(self):
        # Park Switch
        self._ser.write(b'PK\r')

        # Close serial port
        self._ser.close()
