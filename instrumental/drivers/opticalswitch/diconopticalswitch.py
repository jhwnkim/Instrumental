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

class DiConOpticalSwitch(OpticalSwitch):
    _INST_PARAMS_ = ['port']

    def _initialize(self):
        self._ser = Serial(self._paramset['port'], baudrate=115200, timeout=1.0)
        self._channel = 0
        self._channel_max = 16
        self._channel_min = 1
        # *CLS, *RST resets current settings so don't
        # self.write('*CLS')

    def identify(self):
        self._ser.reset_input_buffer()
        self._ser.write(b'ID?\r')
        self._ser.read() # dummy read the newline
        print(self._ser.readline())

    def set_channel(self, new_channel):
        if new_channel >=self._channel_min and new_channel <= self._channel_max:
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
