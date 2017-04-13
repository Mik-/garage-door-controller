from driver import Driver
from blinker import signal
from signals import *
import logging

logger = logging.getLogger('garage.door.' + __name__)

import pigpio 

class PiGpioDriver(Driver):
    """Implements the Driver interface for the Raspberry Pi by pigpio library."""

    def __init__(self, host, gpioRelay, gpioUpperLimitSwitch, gpioLowerLimitSwitch):
        logger.debug("Starting Raspberry PI (pigpio) driver")
        logger.debug(" Relay port        : %d", gpioRelay)
        logger.debug(" Upper limit switch: %d", gpioUpperLimitSwitch)
        logger.debug(" Lower limit switch: %d", gpioLowerLimitSwitch)
        self.gpioRelay = gpioRelay
        self.gpioUpperLimitSwitch = gpioUpperLimitSwitch
        self.gpioLowerLimitSwitch = gpioLowerLimitSwitch

        self.pi = pigpio.pi(host)

        self.pi.set_mode(gpioRelay, pigpio.OUTPUT)
        self.pi.write(gpioRelay, pigpio.LOW)
        
        self.pi.set_mode(gpioUpperLimitSwitch, pigpio.INPUT)
        self.pi.set_pull_up_down(gpioUpperLimitSwitch, pigpio.PUD_UP)
        self.pi.set_glitch_filter(gpioUpperLimitSwitch, 100000)
        self.pi.callback(gpioUpperLimitSwitch, pigpio.EITHER_EDGE, self._handle_switch)
        
        self.pi.set_mode(gpioLowerLimitSwitch, pigpio.INPUT)
        self.pi.set_pull_up_down(gpioLowerLimitSwitch, pigpio.PUD_UP)
        self.pi.set_glitch_filter(gpioLowerLimitSwitch, 100000)
        self.pi.callback(gpioLowerLimitSwitch, pigpio.EITHER_EDGE, self._handle_switch)

    def cleanup(self):
        """Cleanup object, i.e. disconnnect from signals and so on."""
        logger.debug('RPi (pigpio) driver cleanup.')
        self.pi.stop()

    def start_door_signal(self):
        logger.debug("Close relay on port %d", self.gpioRelay)

        self.pi.write(self.gpioRelay, pigpio.HIGH)

    def stop_door_signal(self):
        logger.debug("Open relay on port %d", self.gpioRelay)
        self.pi.write(self.gpioRelay, pigpio.LOW)

    def get_upper_limit_switch_state(self):
        # We have a pull-up resistor installed. If the switch is activated, the
        # signal is pulled to ground.
        return (self.pi.read(self.gpioUpperLimitSwitch) == pigpio.LOW)

    def get_lower_limit_switch_state(self):
        # We have a pull-up resistor installed. If the switch is activated, the
        # signal is pulled to ground.
        return (self.pi.read(self.gpioLowerLimitSwitch) == pigpio.LOW)

    def _handle_switch(self, gpio, level, tick):
        logger.debug("Switch state changed on channel %d", gpio)
        if gpio == self.gpioLowerLimitSwitch:
            switched = signal(SIGNAL_LOWER_SWITCH_CHANGED)
            switched.send(self)
        elif gpio == self.gpioUpperLimitSwitch:
            switched = signal(SIGNAL_UPPER_SWITCH_CHANGED)
            switched.send(self)
