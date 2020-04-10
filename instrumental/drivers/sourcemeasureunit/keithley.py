# -*- coding: utf-8  -*-
"""
Driver for Keithley 2400 Sourcemeter on GPIB communication

Usage Example:
from instrumental.drivers.sourcemeasureunit.keithley import Keithley_2400
smu = Keithley_2400(visa_address='GPIB0::15::INSTR')
smu.identify()
smu.close()
"""

from . import SourceMeasureUnit
from .. import VisaMixin
from ... import Q_

class KeithleySMU(SourceMeasureUnit, VisaMixin):
    _DEFAULT_CURRENT_COMPLIANCE = 0.001 # in A
    _VISA_TIMEOUT = 10000 # in ms

    def _initialize(self):
        sparam.write("*RST")
        time.sleep(1.0)

        # Increase timeout
        self._rsrc.timeout = KeithleySMU._VISA_TIMEOUT

        # initialize variables
        self._voltage = Q_(0.0, 'V') # V
        self._compliance = Q_(KeithleySMU._DEFAULT_CURRENT_COMPLIANCE, 'A')

        # initialize instrument
        self.write("*RST")

        # set voltage source settings
        self.write(':SOUR:FUNC VOLT')
        self.write(':SOUR:SWE:RANG AUTO')
        self.write(':SOUR:VOLT:LEV:AMPL 0.0')

        # set current sense settings
        self.write(':SENS:CURR:PROT {}'.format(KeithleySMU._DEFAULT_CURRENT_COMPLIANCE))
        self.write(':SENS:FUNC "CURR"')
        self.write(':SENS:CURR:RANG:AUTO 1')
        self.write(':SENS:CURR:NPLC 1')

        self.write(':OUTP ON')

    def identify(self):
        print(self.query('*IDN?'))

    def set_integration_time(self, time=1.0):
        """
        Sets the integration time in power-line cycles (16.67 ms)
        :param time: float, 0.01 to 10, 1.0 is default
        :return:
        """
        if time<0.01 or time>10:
            print('KeithleySMU: Specified integration time is not correct. Input 0.01 to 10 power cycles.')
            return
        else:
            self.write(':SENS:CURR:NPLC {:.2f}'.format(time))

    def set_voltage(self, voltage):
        """
        Sets the voltage to the specified value, voltage should be Q_ type
        :return:
        """
        print('Setting Keithley SMU voltage to {:.4f}'.format(voltage))

        self.write(':SOUR:VOLT:LEV:AMPL {:.5E}'.format(voltage.magnitude))

        self._voltage = voltage

    def set_current_compliance(self, compliance):
        """
        :param compliance: In Q_ type
        :return:
        """
        self._compliance = compliance
        self.write(':SENS:CURR:PROT {}'.format(compliance))

    def measure_current(self):
        """
        Measure the current through the device
        :return: The current in A
        """
        try:
            current = Q_(float(self.query("MEASure:CURRent?")), 'A')
        except ValueError:
            current = Q_(0.0, 'A')

        return current

    # Tell list_instruments how to close this VISA resource properly
    @staticmethod
    def _close_resource(resource):
        self.write(':OUTP OFF')

        resource.control_ren(False)  # Disable remote mode

# Models
class Keithley_2400(KeithleySMU):
    _INST_PARAMS_ = ['visa_address']
    _INST_VISA_INFO_ = ('Keithley', ['2400'])
