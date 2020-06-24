
from instrumental.drivers.frequencycounters import FrequencyCounter
from instrumental.drivers import VisaMixin
from instrumental import Q_

class FC53220A(FrequencyCounter, VisaMixin):
    """
    A Keysight 53220A series frequency counter

    Usage Example:
        from instrumental.drivers.frequencycounters.keysight import FC53220A
        smu = HP_4156C(visa_address='GPIB0::17::INSTR')
        smu.identify()
        smu.close()
    """
    _INST_PARAMS_ = ['visa_address']

    def _initialize(self):
      self.resource.read_termination = '\n'

    def frequency(self):
      """The measured frequency"""
      frequency_Hz = float(self.query('MEAS:FREQ?'))
      return Q_(frequency_Hz, 'Hz')

    def period(self):
      """The measured period"""
      period_s = float(self.query('MEAS:PER?'))
      return Q_(period_s, 's')

    def single_period(self, num_counts = 1):
        """Time between triggering events"""
        self.write('SAMP:COUN {}'.format(num_counts))
        self.write('INIT')
        self.write('*WAI')
        time_list = self.query('FETC?') # Read instrument
        singleperiod_s = list(np.float_(time_list.split(","))) # Converts the output string to a float list

        return Q_(singleperiod_s, 's')




    Vthreshold = SCPI_Facet('INP1:LEV ', units='V', type=float, doc="Threshold voltage")
    slope = SCPI_Facet('INP1:SLOP ', type=string, doc="Triggering slope")
    coupling = SCPI_Facet('INP1:COUP ', type=string, doc="Input coupling")
    impedance = SCPI_Facet('INP1:IMP ', units='Ohm', type=int, doc="Input impedance")
