from garage.door.rpi_driver import RPiDriver
import RPi.GPIO as GPIO
import time

driver = RPiDriver(18, 17, 27)

print "RPi-Driver test"
input "Press [Enter] to start test:"

print "The relay is off, the switches are not closed"
input "Press [Enter] to continue:"

print "Close lower limit switch"
while driver.get_lower_limit_switch_state() == False:
    pass

print "Close upper limit switch"
while driver.get_upper_limit_switch_state() == False:
    pass

print "Relais on"
driver.start_door_signal()
time.sleep(2)
print "Relais off"
driver.stop_door_signal()
