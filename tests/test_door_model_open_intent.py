"""
Test the open intent.
"""

import unittest
import time
import logging
from blinker import signal
from garage.door.model import Door
from garage.door.signals import SIGNAL_LOWER_SWITCH_CHANGED, SIGNAL_UPPER_SWITCH_CHANGED
from garage.door.intents import IDLE_INTENT, OPEN_INTENT
from tests.mock_driver import MockDriver

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
        door_model.set_intent(OPEN_INTENT)

        self.assertFalse(mock_driver.door_signal)

        # The command waits the acceleration time, before triggering
        time.sleep(0.3)

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
        self.assertEqual(door_model.intent, IDLE_INTENT)

    def test_state_closed_error(self):
        """
        Test a walk from closed to open with a stuck on first trigger.
        """

        # Door is closed
        mock_driver = MockDriver()
        mock_driver.lower_limit_switch = True
        door_model = Door("Test door", mock_driver, 1, 0.1, 0.2)

        # start intent
        door_model.set_intent(OPEN_INTENT)

        self.assertFalse(mock_driver.door_signal)

        # The command waits the acceleration time, before triggering
        time.sleep(0.3)

        self.assertTrue(mock_driver.door_signal)

        LOGGER.debug("The lower switch didn't open, the door stuck")
        time.sleep(0.2)

        self.assertFalse(mock_driver.door_signal)
        self.assertEqual(door_model.state.__class__.__name__, "ClosedState")
        mock_driver.door_signal_toggled = False

        LOGGER.debug("The intent have to restart the door after timeout")
        time.sleep(0.3)
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
        self.assertEqual(door_model.intent, IDLE_INTENT)

    def test_state_closing(self):
        """Test a walk from closing to open."""

        # Door is closing
        mock_driver = MockDriver()
        door_model = Door("Test door", mock_driver, 1, 0.1, 0.3)
        door_model.set_new_state("Closing")

        # start intent
        door_model.set_intent(OPEN_INTENT)

        # Door should be triggered to stop
        self.assertEqual(mock_driver.trigger_count, 0, "Nothing should be triggerd")
        time.sleep(0.2)
        self.assertEqual(mock_driver.trigger_count, 1, "First trigger to stop the door")

        # Door should be triggered again to start moving up
        time.sleep(0.4)
        self.assertEqual(mock_driver.trigger_count, 2, "Second trigger to start door moving up")

        # After moving, the upper switch closes
        time.sleep(0.5)
        mock_driver.upper_limit_switch = True
        signal(SIGNAL_UPPER_SWITCH_CHANGED).send(mock_driver)
        self.assertEqual(door_model.state.__class__.__name__, "OpenState")
        self.assertEqual(door_model.intent, IDLE_INTENT)
        self.assertEqual(mock_driver.trigger_count, 2, "No additional triggers allowed")
