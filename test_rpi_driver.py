from garage.door.rpi_driver import RPiDriver
import RPi.GPIO as GPIO
import time
from blinker import signal
from garage.door.signals import *


driver = RPiDriver(18, 17, 27)

def switch_status(sender):
    print "Door position: " + driver.get_door_position()

print "RPi-Driver test"
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

signal(SIGNAL_LOWER_SWITCH_CHANGED).disconnect(self._switch_changed)
signal(SIGNAL_UPPER_SWITCH_CHANGED).disconnect(self._switch_changed)

print "Relais on"
driver.start_door_signal()
time.sleep(2)
print "Relais off"
driver.stop_door_signal()
