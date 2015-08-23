from nose.tools import *
from garage.door.model import Door
from mock_driver import MockDriver
from blinker import signal
from garage.door.signals import *
import time

def test_start_opening():
    # Door is closed
    mock_driver = MockDriver()
    mock_driver.lower_limit_switch = True
    door_model = Door("Test door", mock_driver, 1, 0.1, 0.2)

    # trigger move
    door_model.start_door_signal()

    assert mock_driver.door_signal == True

    # The lower switch opened
    mock_driver.lower_limit_switch = False
    signal(SIGNAL_LOWER_SWITCH_CHANGED).send(mock_driver)

    assert mock_driver.door_signal == False
    assert door_model.state.__class__.__name__ == "OpeningState"

def test_start_opening_timeout():
    # Door is closed
    mock_driver = MockDriver()
    mock_driver.lower_limit_switch = True
    door_model = Door("Test door", mock_driver, 1, 0.1, 0.2)

    # trigger move
    door_model.start_door_signal()

    assert mock_driver.door_signal == True

    # The lower switch will not open for two seconds
    # This should expire the trigger timer
    time.sleep(0.2)

    assert mock_driver.door_signal == False
    assert door_model.state.__class__.__name__ == "ClosedState"

def test_start_closing():
    # Door is open
    mock_driver = MockDriver()
    mock_driver.upper_limit_switch = True
    door_model = Door("Test door", mock_driver, 1, 0.1, 0.2)

    # trigger move
    door_model.start_door_signal()

    assert mock_driver.door_signal == True

    # The upper switch opend
    mock_driver.upper_limit_switch = False
    signal(SIGNAL_UPPER_SWITCH_CHANGED).send(mock_driver)

    assert mock_driver.door_signal == False
    assert door_model.state.__class__.__name__ == "ClosingState"

def test_start_closing_timeout():
    # Door is open
    mock_driver = MockDriver()
    mock_driver.upper_limit_switch = True
    door_model = Door("Test door", mock_driver, 1, 0.1, 0.2)

    # trigger move
    door_model.start_door_signal()

    assert mock_driver.door_signal == True

    # The upper switch will not open for 200 ms
    # This should expire the trigger timer (100 ms)
    time.sleep(0.2)

    assert mock_driver.door_signal == False
    assert door_model.state.__class__.__name__ == "OpenState"

def test_opening():
    # Door is closed
    mock_driver = MockDriver()
    door_model = Door("Test door", mock_driver, 0.2, 0.1, 0.2)
    door_model.set_new_state('Opening')

    # The upper switch closed
    mock_driver.upper_limit_switch = True
    signal(SIGNAL_UPPER_SWITCH_CHANGED).send(mock_driver)


    assert door_model.state.__class__.__name__ == "OpenState"
    time.sleep(0.3)
    assert door_model.state.__class__.__name__ == "OpenState"

def test_opening_timeout():
    # Door is closed
    mock_driver = MockDriver()
    door_model = Door("Test door", mock_driver, 0.2, 0.1, 0.2)
    door_model.set_new_state('Opening')

    # The upper switch will not close before timeout is reached
    time.sleep(0.3)

    assert door_model.state.__class__.__name__ == "IntermediateState"

def test_closing():
    # Door is closed
    mock_driver = MockDriver()
    door_model = Door("Test door", mock_driver, 0.2, 0.1, 0.2)
    door_model.set_new_state('Closing')

    # The lower switch closed
    mock_driver.lower_limit_switch = True
    signal(SIGNAL_LOWER_SWITCH_CHANGED).send(mock_driver)

    assert door_model.state.__class__.__name__ == "ClosedState"
    time.sleep(0.3)
    assert door_model.state.__class__.__name__ == "ClosedState"

def test_closing_timeout():
    # Door is closed
    mock_driver = MockDriver()
    door_model = Door("Test door", mock_driver, 0.2, 0.1, 0.2)
    door_model.set_new_state('Closing')

    # The lower switch will not close before timeout is reached
    time.sleep(0.3)

    assert door_model.state.__class__.__name__ == "IntermediateState"

def test_intermediate_to_closed():
    # Door is closed
    mock_driver = MockDriver()
    door_model = Door("Test door", mock_driver, 0.2, 0.1, 0.2)
    door_model.set_new_state('Intermediate')

    # The lower switch closed
    mock_driver.lower_limit_switch = True
    signal(SIGNAL_LOWER_SWITCH_CHANGED).send(mock_driver)

    assert door_model.state.__class__.__name__ == "ClosedState"

def test_intermediate_to_open():
    # Door is closed
    mock_driver = MockDriver()
    door_model = Door("Test door", mock_driver, 0.2, 0.1, 0.2)
    door_model.set_new_state('Intermediate')

    # The upper switch closed
    mock_driver.upper_limit_switch = True
    signal(SIGNAL_UPPER_SWITCH_CHANGED).send(mock_driver)

    assert door_model.state.__class__.__name__ == "OpenState"

def test_error():
    # Door is closed
    mock_driver = MockDriver()
    door_model = Door("Test door", mock_driver, 0.2, 0.1, 0.2)

    # Both switches closed
    mock_driver.upper_limit_switch = True
    signal(SIGNAL_UPPER_SWITCH_CHANGED).send(mock_driver)
    mock_driver.lower_limit_switch = True
    signal(SIGNAL_LOWER_SWITCH_CHANGED).send(mock_driver)

    assert door_model.state.__class__.__name__ == "ErrorState"
