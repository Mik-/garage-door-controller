from driver import Driver
from blinker import signal
from signals import *
import logging

logger = logging.getLogger('garage.door.' + __name__)

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    logger.error("Error importing RPi.GPIO")
    print("Error importing RPi.GPIO!  This is probably because you need " +
        "superuser privileges.  You can achieve this by using 'sudo' to run " +
        "your script")

class RPiDriver(Driver):
    """Implements the Driver interface for the Raspberry Pi."""

    def __init__(self, gpioRelay, gpioUpperLimitSwitch, gpioLowerLimitSwitch):
        logger.debug("Starting Raspberry PI driver")
        logger.debug(" Relay port        : %d", gpioRelay)
        logger.debug(" Upper limit switch: %d", gpioUpperLimitSwitch)
        logger.debug(" Lower limit switch: %d", gpioLowerLimitSwitch)
        self.gpioRelay = gpioRelay
        self.gpioUpperLimitSwitch = gpioUpperLimitSwitch
        self.gpioLowerLimitSwitch = gpioLowerLimitSwitch

        GPIO.setmode(GPIO.BCM);
        GPIO.setup(self.gpioRelay, GPIO.OUT)
        GPIO.output(self.gpioRelay, GPIO.LOW)
        GPIO.setup(self.gpioUpperLimitSwitch, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.gpioLowerLimitSwitch, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        GPIO.add_event_detect(self.gpioUpperLimitSwitch, GPIO.BOTH, callback=self._handle_switch, bouncetime=200)
        GPIO.add_event_detect(self.gpioLowerLimitSwitch, GPIO.BOTH, callback=self._handle_switch, bouncetime=200)

    def cleanup(self):
        """Cleanup object, i.e. disconnnect from signals and so on."""
        logger.debug('RPi driver cleanup.')
        GPIO.cleanup([self.gpioRelay, self.gpioUpperLimitSwitch,
            self.gpioLowerLimitSwitch])

    def start_door_signal(self):
        logger.debug("Close relay on port %d", self.gpioRelay)
        GPIO.output(self.gpioRelay, GPIO.HIGH)

    def stop_door_signal(self):
        logger.debug("Open relay on port %d", self.gpioRelay)
        GPIO.output(self.gpioRelay, GPIO.LOW)

    def get_upper_limit_switch_state(self):
        # We have a pull-up resistor installed. If the switch is activated, the
        # signal is pulled to ground.
        return (GPIO.input(self.gpioUpperLimitSwitch) == GPIO.LOW)

    def get_lower_limit_switch_state(self):
        # We have a pull-up resistor installed. If the switch is activated, the
        # signal is pulled to ground.
        return (GPIO.input(self.gpioLowerLimitSwitch) == GPIO.LOW)

    def _handle_switch(self, channel):
        logger.debug("Switch state changed on channel %d", channel)
        if channel == self.gpioLowerLimitSwitch:
            switched = signal(SIGNAL_LOWER_SWITCH_CHANGED)
            switched.send(self)
        elif channel == self.gpioUpperLimitSwitch:
            switched = signal(SIGNAL_UPPER_SWITCH_CHANGED)
            switched.send(self)
