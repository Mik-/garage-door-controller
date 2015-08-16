from nose.tools import *
from garage.door.model import Door
from mock_driver import MockDriver

def test_init_setup_error_state():
    mock_driver = MockDriver()
    door_model = Door("Test door", mock_driver, 1, 1)

    assert door_model.state.__class__.__name__ == "IntermediateState"

def test_init_error_state():
    mock_driver = MockDriver()
    mock_driver.upper_limit_switch = True
    mock_driver.lower_limit_switch = True
    door_model = Door("Test door", mock_driver, 1, 1)

    assert door_model.state.__class__.__name__ == "ErrorState"

def test_init_open_state():
    mock_driver = MockDriver()
    mock_driver.upper_limit_switch = True
    door_model = Door("Test door", mock_driver, 1, 1)

    assert door_model.state.__class__.__name__ == "OpenState"

def test_init_closed_state():
    mock_driver = MockDriver()
    mock_driver.lower_limit_switch = True
    door_model = Door("Test door", mock_driver, 1, 1)

    assert door_model.state.__class__.__name__ == "ClosedState"
