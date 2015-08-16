from driver import Driver
from signlas import *

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need " +
        "superuser privileges.  You can achieve this by using 'sudo' to run " +
        "your script")

class RPiDriver(Driver)
    """Implements the Driver interface for the Raspberry Pi."""

    def __init__(self, gpioRelais, gpioUpperLimitSwitch, gpioLowerLimitSwitch):
        self.gpioRelais = gpioRelais
        self.gpioUpperLimitSwitch = gpioUpperLimitSwitch
        self.gpioLowerLimitSwitch = gpioLowerLimitSwitch

        GPIO.setmode(GPIO.BCM);
        GPIO.setup(self.gpioRelais, GPIO.OUT)
        GPIO.output(self.gpioRelais, GPIO.LOW)
        GPIO.setup(self.gpioUpperLimitSwitch, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.gpioLowerLimitSwitch, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        GPIO.add_event_detected(self.gpioUpperLimitSwitch, GPIO.RISING, callback=self._handle_switch, bouncetime=200)
        GPIO.add_event_detected(self.gpioUpperLimitSwitch, GPIO.FALLING, callback=self._handle_switch, bouncetime=200)
        GPIO.add_event_detected(self.gpioLowerLimitSwitch, GPIO.RISING, callback=self._handle_switch, bouncetime=200)
        GPIO.add_event_detected(self.gpioLowerLimitSwitch, GPIO.FALLING, callback=self._handle_switch, bouncetime=200)

    def __del__(self):
        GPIO.cleanup([self.gpioRelais, self.gpioUpperLimitSwitch,
            self.gpioLowerLimitSwitch])

    def start_door_signal(self):
        GPIO.output(self.gpioRelais, GPIO.HIGH)

    def stop_door_signal(self):
        GPIO.output(self.gpioRelais, GPIO.LOW)

    def get_upper_limit_switch_state(self):
        # We have a pull-up resistor installed. If the switch is activated, the
        # signal is pulled to ground.
        return (GPIO.input(self.gpioUpperLimitSwitch) == GPIO.LOW)

    def get_lower_limit_switch_state(self):
        # We have a pull-up resistor installed. If the switch is activated, the
        # signal is pulled to ground.
        return (GPIO.input(self.gpioLowerLimitSwitch) == GPIO.LOW)

    def _handle_switch(self, channel):
        if channel == self.gpioLowerLimitSwitch:
            switched = signal(SIGNAL_LOWER_SWITCH_CHANGED)
            switched.send(self)
        elif channel == self.gpioUpperLimitSwitch:
            switched = signal(SIGNAL_UPPER_SWITCH_CHANGED)
            switched.send(self)
