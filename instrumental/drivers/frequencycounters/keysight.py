from instrumental.drivers.powermeters import FrequencyCounter
from instrumental.drivers import VisaMixin

class FC53220A(FrequencyCounter, VisaMixin):
    """A Keysight 53220A series frequency counter"""
    _INST_PARAMS_ = ['visa_address']
