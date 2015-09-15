from nose.tools import *
from garage.door.model import Door
from perfect_door_driver import PerfectDoorDriver
from blinker import signal
from garage.door.signals import *
import time

def test_perfect_door():
    # Door is closed
    driver = PerfectDoorDriver(0.4, 0.15)
    door_model = Door("Test door", driver, 0.5, 0.1, 0.2)

    # The door is closed and idle   
    assert door_model.state.__class__.__name__ == 'ClosedState'
    assert door_model.intent.__class__.__name__ == 'IdleIntent'
    # Set "open" intent
    door_model.set_intent('Open');
    assert door_model.intent.__class__.__name__ == 'OpenIntent'
    assert driver.door_signal == True
    time.sleep(0.2)
    # After 0.15 seconds, the door should be in transit to upper position
    assert driver.door_signal == False
    assert door_model.state.__class__.__name__ == 'OpeningState'
    assert door_model.intent.__class__.__name__ == 'OpenIntent'
    assert driver.lower_limit_switch == False
    assert driver.upper_limit_switch == False
    time.sleep(0.25)
    # After 0.4 seconds, the door should be in upper position
    assert door_model.state.__class__.__name__ == 'OpenState'
    assert door_model.intent.__class__.__name__ == 'IdleIntent'
    assert driver.upper_limit_switch == True

    # The door is open and idle
    # Set "close" intent
    door_model.set_intent('Close');
    assert door_model.intent.__class__.__name__ == 'CloseIntent'
    assert driver.door_signal == True
    time.sleep(0.2)
    # After 0.15 seconds, the door should be in transit to lower position
    assert driver.door_signal == False
    assert door_model.state.__class__.__name__ == 'ClosingState'
    assert door_model.intent.__class__.__name__ == 'CloseIntent'
    assert driver.lower_limit_switch == False
    assert driver.upper_limit_switch == False
    time.sleep(0.25)
    # After 0.4 seconds, the door should be in lower position
    assert door_model.state.__class__.__name__ == 'ClosedState'
    assert door_model.intent.__class__.__name__ == 'IdleIntent'
    assert driver.lower_limit_switch == True
