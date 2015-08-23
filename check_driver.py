from garage.door.rpi_driver import RPiDriver
import RPi.GPIO as GPIO
import time
from blinker import signal
from garage.door.signals import *

# Setup the driver for the specified gpios
# 18 relay
# 17 lower limit switch
# 27 upper limit switch
driver = RPiDriver(18, 17, 27)

def switch_status(sender):
    """This is a callable, which is called on edge detection by the driver."""
    print "Upper limit switch: %r" % driver.get_upper_limit_switch_state()
    print "Lower limit switch: %r" % driver.get_lower_limit_switch_state()


print "Driver test"
raw_input("Press [Enter] to start test")

print "The relay is off, the switches are not closed"
raw_input("Press [Enter] to continue")

signal(SIGNAL_LOWER_SWITCH_CHANGED).connect(switch_status)
signal(SIGNAL_UPPER_SWITCH_CHANGED).connect(switch_status)

print "Close lower limit switch"
while driver.get_lower_limit_switch_state() == False:
    pass

print "Close upper limit switch"
while driver.get_upper_limit_switch_state() == False:
    pass

signal(SIGNAL_LOWER_SWITCH_CHANGED).disconnect(switch_status)
signal(SIGNAL_UPPER_SWITCH_CHANGED).disconnect(switch_status)

print "Relais on"
driver.start_door_signal()
time.sleep(2)
print "Relais off"
driver.stop_door_signal()
