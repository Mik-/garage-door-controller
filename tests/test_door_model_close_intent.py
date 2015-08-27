from nose.tools import *
from garage.door.model import Door
from mock_driver import MockDriver
from blinker import signal
from garage.door.signals import *
import time
import logging

logger = logging.getLogger(__name__)

def test_state_opened():
    # Door is open
    mock_driver = MockDriver()
    mock_driver.upper_limit_switch = True
    door_model = Door("Test door", mock_driver, 1, 0.1, 0.2)

    # start intent
    door_model.set_intent("Close");

    assert mock_driver.door_signal == True

    logger.debug("The upper switch opened")
    mock_driver.upper_limit_switch = False
    signal(SIGNAL_UPPER_SWITCH_CHANGED).send(mock_driver)

    assert mock_driver.door_signal == False
    assert door_model.state.__class__.__name__ == "ClosingState"

    logger.debug("The lower switch closed")
    mock_driver.lower_limit_switch = True
    signal(SIGNAL_LOWER_SWITCH_CHANGED).send(mock_driver)

    assert door_model.state.__class__.__name__ == "ClosedState"
    assert door_model.intent.__class__.__name__ == "IdleIntent"

def test_state_open_error():
    # Door is open
    mock_driver = MockDriver()
    mock_driver.upper_limit_switch = True
    door_model = Door("Test door", mock_driver, 1, 0.1, 0.3)

    # start intent
    door_model.set_intent("Close");

    assert mock_driver.door_signal == True

    logger.debug("The upper switch didn't open, the door stuck")
    time.sleep(0.2)

    assert mock_driver.door_signal == False
    assert door_model.state.__class__.__name__ == "OpenState"
    mock_driver.door_signal_toggled = False

    logger.debug("The intent have to restart the door after timeout")
    time.sleep(0.2)
    assert mock_driver.door_signal_toggled == True

    logger.debug("The intent have restart the door after timeout")

    logger.debug("Now the upper switch opened")
    mock_driver.upper_limit_switch = False
    signal(SIGNAL_UPPER_SWITCH_CHANGED).send(mock_driver)

    assert mock_driver.door_signal == False
    assert door_model.state.__class__.__name__ == "ClosingState"

    logger.debug("The lower switch closed")
    mock_driver.lower_limit_switch = True
    signal(SIGNAL_LOWER_SWITCH_CHANGED).send(mock_driver)

    assert door_model.state.__class__.__name__ == "ClosedState"
    assert door_model.intent.__class__.__name__ == "IdleIntent"
