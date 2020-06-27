# -*- coding: utf-8  -*-
"""
Driver module for HP Lightwave power meters. Supports:

* HP Lightwave8153A
Usage Example:
from instrumental.drivers.powermeters.hp import HP_8153A
pm = HP_8153A(visa_address='GPIB0::15::INSTR')
pm.identify()
pm.close()

"""

from . import PowerMeter
from .. import VisaMixin, SCPI_Facet
from ... import Q_


class HP_8153A(PowerMeter, VisaMixin):
    """HP Lightwave 8153A power meter"""
    _INST_PARAMS_ = ['visa_address']
    _INST_VISA_INFO_ = ('HP Lightwave', ['8153A'])

    def _initialize(self):
        self._rsrc.read_termination = '\n'
        self._rsrc.timeout = 20000 # ms timeout

        # initialize internal Variables
        self.tap_channel = 1
        self.rec_channel = 2
        self.int_time = 0.05 # seconds

        # Set units to W
        self.write("SENS:POW:UNIT 1")
        # self.write("SENS%d:CHAN1:POW:UNIT 1" % self.rec_channel)

        # Automatic power range
        self.write("SENS:POW:RANG:AUTO 1" % self.tap_channel)
        # self.write("SENS%d:CHAN1:POW:RANG:AUTO 1" % self.rec_channel)

        # Set integration time
        self.write("SENS:POW:ATIME %.3fS" % self.int_time)
        # self.write("SENS%d:CHAN1:POW:ATIME %.3fS" % (self.rec_channel, self.int_time))

        # Do not measure continuously
        self.write("INIT:CONT 0")
        # self.write("INIT%d:CHAN1:CONT 0" % self.rec_channel)

    def identify(self):
        print(self.query('*IDN?'))

    def close(self):
        self._rsrc.control_ren(False)  # Disable remote mode

    # Tell list_instruments how to close this VISA resource properly
    @staticmethod
    def _close_resource(resource):
        resource.control_ren(False)  # Disable remote mode

    # power = SCPI_Facet('POW', units='W', readonly=True, type=float,
    #                         doc="Measured Power")
    # Not using SCPI_Facet because the value gets stuck when auto ranging
    def power(self):
        self.write("INIT1:IMM")
        try:
            meas_power = max(0.0, float(self.query('FETC1:POW?')))
        except ValueError:
            meas_power = 0.0

        return Q_(meas_power, units='W')

    wavelength = SCPI_Facet('SENS1:POW:WAVE', units='nm', type=float,
                            doc="Input signal wavelength")

    auto_range = SCPI_Facet('SENS1:POW:RANG:AUTO', convert=int, value={False:0, True:1},
                            doc="Whether auto-ranging is enabled")

    integration_time = SCPI_Facet('SEN1:POW:ATIME', units='s', type=float,
                            doc="Measurement integration time in seconds 20ms to 3600s available")
