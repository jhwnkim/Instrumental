# -*- coding: utf-8  -*-
"""
Driver for HP 4156C on GPIB communication

Usage Example:
from instrumental.drivers.sourcemeasureunit.hp import HPSemiParamAnalyzer
smu = HPSemiParamAnalyzer(visa_address='GPIB0::17::INSTR')
switch.identify()
switch.close()
"""

from . import SourceMeasureUnit
from .. import VisaMixin, SCPI_Facet

class HPSemiParamAnalyzer(SourceMeasureUnit, VisaMixin):
    _INST_PARAMS_ = ['visa_address']
    _INST_VISA_INFO = {
        'HpSemiParamAnalyzer': ('HEWLETT-PACKARD', ['4156C'])
    }

    def _initialize(self):
        self._rsrc.read_termination = '\r'
        self._rsrc.write_termination = '\n'
        # *CLS, *RST resets current settings so don't
        # self.write('*CLS')

    def identify(self):
        print(self.query('*IDN?'))

    channel = SCPI_Facet(':ROUTE:OPEN', convert=int)
    polarity = SCPI_Facet(':ROUTE:POLARITY', convert=int)

    lamp = SCPI_Facet(':LAMP:OUT', convert=int)

    # Tell list_instruments how to close this VISA resource properly
    @staticmethod
    def _close_resource(resource):
        channel = 0 # Close all channels
        lamp = 0 # Turns off lamp
        resource.control_ren(False)  # Disable remote mode
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
