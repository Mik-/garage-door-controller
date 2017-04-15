"""
Test the door switching.
"""

import unittest
import time
from blinker import signal
from garage.door.model import Door
from garage.door.signals import SIGNAL_LOWER_SWITCH_CHANGED, SIGNAL_UPPER_SWITCH_CHANGED
from mock_driver import MockDriver

class TestDoorModelSwitching(unittest.TestCase):
    """
    Tests the door switching.
    """

    def test_start_opening(self):
        """
        The door is closed. After a trigger, it should be in opening state.
        """

        # Door is closed
        mock_driver = MockDriver()
        mock_driver.lower_limit_switch = True
        door_model = Door("Test door", mock_driver, 1, 0.1, 0.2)

        # trigger move
        door_model.start_door_signal()

        self.assertTrue(mock_driver.door_signal)

        # The lower switch opened
        mock_driver.lower_limit_switch = False
        signal(SIGNAL_LOWER_SWITCH_CHANGED).send(mock_driver)

        self.assertFalse(mock_driver.door_signal)
        self.assertEqual(door_model.state.__class__.__name__, "OpeningState")

    def test_start_opening_timeout(self):
        """
        The door is closed. After a trigger an not opening the door,
        the relay should not be triggerd after timeout.
        """

        # Door is closed
        mock_driver = MockDriver()
        mock_driver.lower_limit_switch = True
        door_model = Door("Test door", mock_driver, 1, 0.1, 0.2)

        # trigger move
        door_model.start_door_signal()

        self.assertTrue(mock_driver.door_signal)

        # The lower switch will not open for two seconds
        # This should expire the trigger timer
        time.sleep(0.2)

        self.assertFalse(mock_driver.door_signal)
        self.assertEqual(door_model.state.__class__.__name__, "ClosedState")

    def test_start_closing(self):
        """
        The door is open. After trigger, it should be in closing state.
        """
        # Door is open
        mock_driver = MockDriver()
        mock_driver.upper_limit_switch = True
        door_model = Door("Test door", mock_driver, 1, 0.1, 0.2)

        # trigger move
        door_model.start_door_signal()

        self.assertTrue(mock_driver.door_signal)

        # The upper switch opend
        mock_driver.upper_limit_switch = False
        signal(SIGNAL_UPPER_SWITCH_CHANGED).send(mock_driver)

        self.assertFalse(mock_driver.door_signal)
        self.assertEqual(door_model.state.__class__.__name__, "ClosingState")

    def test_start_closing_timeout(self):
        """
        The door is open. After trigger and not moving and a timeout, the
        relay should not be active.
        """

        # Door is open
        mock_driver = MockDriver()
        mock_driver.upper_limit_switch = True
        door_model = Door("Test door", mock_driver, 1, 0.1, 0.2)

        # trigger move
        door_model.start_door_signal()

        self.assertTrue(mock_driver.door_signal)

        # The upper switch will not open for 200 ms
        # This should expire the trigger timer (100 ms)
        time.sleep(0.2)

        self.assertFalse(mock_driver.door_signal)
        self.assertEqual(door_model.state.__class__.__name__, "OpenState")

    def test_opening(self):
        """
        The door is opening. After reaching the upper limit, it should be in open state.
        """

        # Door is closed
        mock_driver = MockDriver()
        door_model = Door("Test door", mock_driver, 0.2, 0.1, 0.2)
        door_model.set_new_state('Opening')

        # The upper switch closed
        mock_driver.upper_limit_switch = True
        signal(SIGNAL_UPPER_SWITCH_CHANGED).send(mock_driver)


        self.assertEqual(door_model.state.__class__.__name__, "OpenState")
        time.sleep(0.3)
        self.assertEqual(door_model.state.__class__.__name__, "OpenState")

    def test_opening_timeout(self):
        """
        The door is opening. After transit time and not reaching upper limit,
        it should change to intermediate state.
        """

        # Door is closed
        mock_driver = MockDriver()
        door_model = Door("Test door", mock_driver, 0.2, 0.1, 0.2)
        door_model.set_new_state('Opening')

        # The upper switch will not close before timeout is reached
        time.sleep(0.3)

        self.assertEqual(door_model.state.__class__.__name__, "IntermediateState")

    def test_closing(self):
        """
        The door is closing. After reaching lower limit, it should change to closed state.
        """
        # Door is closed
        mock_driver = MockDriver()
        door_model = Door("Test door", mock_driver, 0.2, 0.1, 0.2)
        door_model.set_new_state('Closing')

        # The lower switch closed
        mock_driver.lower_limit_switch = True
        signal(SIGNAL_LOWER_SWITCH_CHANGED).send(mock_driver)

        self.assertEqual(door_model.state.__class__.__name__, "ClosedState")
        time.sleep(0.3)
        self.assertEqual(door_model.state.__class__.__name__, "ClosedState")

    def test_closing_timeout(self):
        """
        The door is closing. After transit time and not reaching the lower limit,
        it should switch to intermediate state.
        """

        # Door is closed
        mock_driver = MockDriver()
        door_model = Door("Test door", mock_driver, 0.2, 0.1, 0.2)
        door_model.set_new_state('Closing')

        # The lower switch will not close before timeout is reached
        time.sleep(0.3)

        self.assertEqual(door_model.state.__class__.__name__, "IntermediateState")

    def test_intermediate_to_closed(self):
        """
        The door is in intermediate state. After reaching the lower limit,
        it should change to closed state.
        """

        # Door is closed
        mock_driver = MockDriver()
        door_model = Door("Test door", mock_driver, 0.2, 0.1, 0.2)
        door_model.set_new_state('Intermediate')

        # The lower switch closed
        mock_driver.lower_limit_switch = True
        signal(SIGNAL_LOWER_SWITCH_CHANGED).send(mock_driver)

        self.assertEqual(door_model.state.__class__.__name__, "ClosedState")

    def test_intermediate_to_open(self):
        """
        The door is in intermediate state. After reaching the upper limit,
        it should change to open state.
        """

        # Door is closed
        mock_driver = MockDriver()
        door_model = Door("Test door", mock_driver, 0.2, 0.1, 0.2)
        door_model.set_new_state('Intermediate')

        # The upper switch closed
        mock_driver.upper_limit_switch = True
        signal(SIGNAL_UPPER_SWITCH_CHANGED).send(mock_driver)

        self.assertEqual(door_model.state.__class__.__name__, "OpenState")

    def test_error(self):
        """
        The door should change to error state, if upper and lower limit
        switches are both closed.
        """

        # Door is closed
        mock_driver = MockDriver()
        door_model = Door("Test door", mock_driver, 0.2, 0.1, 0.2)

        # Both switches closed
        mock_driver.upper_limit_switch = True
        signal(SIGNAL_UPPER_SWITCH_CHANGED).send(mock_driver)
        mock_driver.lower_limit_switch = True
        signal(SIGNAL_LOWER_SWITCH_CHANGED).send(mock_driver)

        self.assertEqual(door_model.state.__class__.__name__, "ErrorState")
