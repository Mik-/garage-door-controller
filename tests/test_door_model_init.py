"""
Tests the door initialization.
"""

import unittest
from garage.door.model import Door
from mock_driver import MockDriver

class TestDoorModelInit(unittest.TestCase):
    """
    Tests the door initialization.
    """

    def test_init_setup_error_state(self):
        """
        The initialized mock driver is in intermediate state, so the state
        of the door should also be in intermediate state after initialization.
        """

        mock_driver = MockDriver()
        door_model = Door("Test door", mock_driver, 1, 1, 2)

        self.assertEqual(door_model.state.__class__.__name__, "IntermediateState")

    def test_init_error_state(self):
        """
        Pretend, both limit switches are closed. This result in the error state.
        """

        mock_driver = MockDriver()
        mock_driver.upper_limit_switch = True
        mock_driver.lower_limit_switch = True
        door_model = Door("Test door", mock_driver, 1, 1, 2)

        self.assertEqual(door_model.state.__class__.__name__, "ErrorState")

    def test_init_open_state(self):
        """
        Pretend, the door is open. This should result in open state.
        """

        mock_driver = MockDriver()
        mock_driver.upper_limit_switch = True
        door_model = Door("Test door", mock_driver, 1, 1, 2)

        self.assertEqual(door_model.state.__class__.__name__, "OpenState")

    def test_init_closed_state(self):
        """
        Pretend, the door is closed. This should result in closed state.
        """

        mock_driver = MockDriver()
        mock_driver.lower_limit_switch = True
        door_model = Door("Test door", mock_driver, 1, 1, 2)

        self.assertEqual(door_model.state.__class__.__name__, "ClosedState")
