"""
Test the open intent.
"""

import unittest
import time
import logging
from blinker import signal
from garage.door.model import Door
from garage.door.signals import SIGNAL_LOWER_SWITCH_CHANGED, SIGNAL_UPPER_SWITCH_CHANGED
from mock_driver import MockDriver

LOGGER = logging.getLogger(__name__)

class TestDoorModelOpenIntent(unittest.TestCase):
    """
    Test the open intent.
    """

    def test_state_closed(self):
        """
        Test a perfect walk from closed to open.
        """

        # Door is closed
        mock_driver = MockDriver()
        mock_driver.lower_limit_switch = True
        door_model = Door("Test door", mock_driver, 1, 0.1, 0.2)

        # start intent
        door_model.set_intent("Open")

        self.assertTrue(mock_driver.door_signal)

        LOGGER.debug("The lower switch opened")
        mock_driver.lower_limit_switch = False
        signal(SIGNAL_LOWER_SWITCH_CHANGED).send(mock_driver)

        self.assertFalse(mock_driver.door_signal)
        self.assertEqual(door_model.state.__class__.__name__, "OpeningState")

        LOGGER.debug("The upper switch closed")
        mock_driver.upper_limit_switch = True
        signal(SIGNAL_UPPER_SWITCH_CHANGED).send(mock_driver)

        self.assertEqual(door_model.state.__class__.__name__, "OpenState")
        self.assertEqual(door_model.intent.__class__.__name__, "IdleIntent")

    def test_state_closed_error(self):
        """
        Test a walk from closed to open with a stuck on first trigger.
        """

        # Door is closed
        mock_driver = MockDriver()
        mock_driver.lower_limit_switch = True
        door_model = Door("Test door", mock_driver, 1, 0.1, 0.3)

        # start intent
        door_model.set_intent("Open")

        self.assertTrue(mock_driver.door_signal)

        LOGGER.debug("The lower switch didn't open, the door stuck")
        time.sleep(0.2)

        self.assertFalse(mock_driver.door_signal)
        self.assertEqual(door_model.state.__class__.__name__, "ClosedState")
        mock_driver.door_signal_toggled = False

        LOGGER.debug("The intent have to restart the door after timeout")
        time.sleep(0.2)
        self.assertTrue(mock_driver.door_signal_toggled)

        LOGGER.debug("The intent have restart the door after timeout")

        LOGGER.debug("Now the lower switch opened")
        mock_driver.lower_limit_switch = False
        signal(SIGNAL_LOWER_SWITCH_CHANGED).send(mock_driver)

        self.assertFalse(mock_driver.door_signal)
        self.assertEqual(door_model.state.__class__.__name__, "OpeningState")

        LOGGER.debug("The upper switch closed")
        mock_driver.upper_limit_switch = True
        signal(SIGNAL_UPPER_SWITCH_CHANGED).send(mock_driver)

        self.assertEqual(door_model.state.__class__.__name__, "OpenState")
        self.assertEqual(door_model.intent.__class__.__name__, "IdleIntent")
