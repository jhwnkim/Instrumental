# -*- coding: utf-8  -*-
# Copyright 2020 Nili Persits and Jaehwan Kim
"""
Driver for M2 Solstis Tunable Laser

This driver talks to ICE BLOC the controller for the Solstis laser through TCP/IP sockets

Usage Example:
from instrumental.drivers.lasers.solstis import M2_Solstis
laser = M2_Solstis(client_ip='192.168.1.100', port=9001, address='localhost')
laser.identify()
laser.set_wavelength(wavelength=850.0)
print( laser.get_wavelength() )
laser.close()
"""
from . import Laser

_INST_PARAMS = ['client_ip', 'port', 'address']

class M2_Solstis(Laser):
    """ A M2 Solstis tunable laser.

    client_ip :
    port : Port
    address : Address to 
    """

    def _initialize(self):
        pass

    def is_control_on(self):
        """ Returns the status of the hardware input control.

        Hardware input control must be on in order for the laser to be
        controlled by usb connection.

        Returns
        -------
        message : bool
            If True, hardware input conrol is on.
        """
        message = self._ask('(param-ref hw-input-dis)')
        message = bool_dict[message]
        return message

    def set_control(self, control):
        """ Sets the status of the hardware input control.

        Hardware input control must be on in order for the laser to be
        controlled by usb connection.

        Parameters
        ----------
        control : bool
            If True, hardware input conrol is turned on.

        Returns
        -------
        error : int or str
            Zero is returned if the hardware input control status was set
            correctly.  Otherwise, the error string returned by the laser
            is returned.
        """
        for key, item in bool_dict.iteritems():
            if item == control:
                control = key
        error = self._ask('(param-set! hw-input-dis {})'.format(control),
                          return_error=True)
        return error

    def is_on(self):
        """
        Indicates if the laser is on (True) or off (False).
        """
        message = self._ask('(param-ref laser:en)')
        message = bool_dict[message]
        return message

    def _set_emission(self, control):
        """ Sets the emission status of the laser.

        Parameters
        ----------
        control : bool
            If True, the laser output is turned on.  If False, the laser output
            is turned off.

        Returns
        -------
        error : int or str
            Zero is returned if the emission status was set
            correctly.  Otherwise, the error string returned by the laser
            is returned.
        """
        for key, item in bool_dict.iteritems():
            if item == control:
                control = key
        error = self._ask('(param-set! laser:en {})'.format(control),
                          return_error=True)
        return error

    def turn_on(self):
        """ Turns the laser on.

        Note that hardware control must be enabled in order for this method
        to execute properly.

        Returns
        -------
        error : int or str
            Zero is returned if the laser was successfuly turned on.
            Otherwise, the error string returned by the laser is returned.
        """
        return self._set_emission(True)

    def turn_off(self):
        """  Turns the laser off.

        Note that hardware control must be enabled in order for this method
        to execute properly.

        Returns
        -------
        error : int or str
            Zero is returned if the laser was correctly turned off.
            Otherwise, the error string returned by the laser is returned.
        """
        return self._set_emission(False)

    def _ask(self, message, return_error=False):
        self._rsrc.ask(message)
        message = self._rsrc.read(termination='\n')
        if return_error:
            error = message
            if error == '0':
                error = int(error)
            return error
        return message

    def close(self):
        """
        Closes the connection to the laser.
        """
        self._rsrc.close()
