from nose.tools import *
from garage.door.model import Door
from stuck_door_driver import StuckDoorDriver
from blinker import signal
from garage.door.signals import *
import time

def test_stuck_door():
    # Door is closed
    driver = StuckDoorDriver(0.4, 0.15)
    door_model = Door("Test door", driver, 0.5, 0.1, 0.2)

    # The door is closed and idle
    assert door_model.state.__class__.__name__ == 'ClosedState'
    assert door_model.intent.__class__.__name__ == 'IdleIntent'
    # Set "open" intent
    door_model.set_intent('Open');
    assert door_model.intent.__class__.__name__ == 'OpenIntent'
    assert driver.door_signal == True
    time.sleep(0.175)
    # After 0.15 seconds, the door stucks in lower position
    assert driver.door_signal == False
    assert door_model.state.__class__.__name__ == 'ClosedState'
    assert door_model.intent.__class__.__name__ == 'OpenIntent'
    assert driver.lower_limit_switch == True
    assert driver.upper_limit_switch == False
    time.sleep(0.05)
    # After 0.2 seconds, the door should be triggered once more
    assert driver.door_signal == True
    time.sleep(0.2)
    # After 0.4 seconds, the door should be in transit to upper position
    assert driver.door_signal == False
    assert door_model.state.__class__.__name__ == 'OpeningState'
    assert door_model.intent.__class__.__name__ == 'OpenIntent'
    assert driver.lower_limit_switch == False
    assert driver.upper_limit_switch == False
