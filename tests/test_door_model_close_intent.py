"""
Test the close intent.
"""

import unittest
import time
import logging
from blinker import signal
from garage.door.model import Door
from garage.door.signals import SIGNAL_LOWER_SWITCH_CHANGED, SIGNAL_UPPER_SWITCH_CHANGED
from garage.door.intents import IDLE_INTENT, CLOSE_INTENT
from mock_driver import MockDriver

LOGGER = logging.getLogger(__name__)

class TestDoorModelCloseIntent(unittest.TestCase):
    """
    Tests the close intent.
    """

    def test_state_opened(self):
        """
        Test a perfect door walk from open to closed by setting the intent.
        """

        # Door is open
        mock_driver = MockDriver()
        mock_driver.upper_limit_switch = True
        door_model = Door("Test door", mock_driver, 1, 0.1, 0.2)

        # start intent
        door_model.set_intent(CLOSE_INTENT)

        self.assertFalse(mock_driver.door_signal)
        time.sleep(0.3)
        self.assertTrue(mock_driver.door_signal)

        LOGGER.debug("The upper switch opened")
        mock_driver.upper_limit_switch = False
        signal(SIGNAL_UPPER_SWITCH_CHANGED).send(mock_driver)

        self.assertFalse(mock_driver.door_signal)
        self.assertEqual(door_model.state.__class__.__name__, "ClosingState")

        LOGGER.debug("The lower switch closed")
        mock_driver.lower_limit_switch = True
        signal(SIGNAL_LOWER_SWITCH_CHANGED).send(mock_driver)

        self.assertEqual(door_model.state.__class__.__name__, "ClosedState")
        self.assertEqual(door_model.intent, IDLE_INTENT)

    def test_state_open_error(self):
        """
        Test a door walk from open to closed by setting the intent and
        a stuck on first trigger event.
        """

        # Door is open
        mock_driver = MockDriver()
        mock_driver.upper_limit_switch = True
        door_model = Door("Test door", mock_driver, 1, 0.1, 0.2)

        # start intent
        door_model.set_intent(CLOSE_INTENT)

        self.assertTrue(mock_driver.door_signal)

        LOGGER.debug("The upper switch didn't open, the door stuck")
        time.sleep(0.2)

        self.assertFalse(mock_driver.door_signal)
        self.assertEqual(door_model.state.__class__.__name__, "OpenState")
        mock_driver.door_signal_toggled = False

        LOGGER.debug("The intent has to restart the door after timeout")
        time.sleep(0.2)
        self.assertTrue(mock_driver.door_signal_toggled)

        LOGGER.debug("The intent has restart the door after timeout")

        LOGGER.debug("Now the upper switch opened")
        mock_driver.upper_limit_switch = False
        signal(SIGNAL_UPPER_SWITCH_CHANGED).send(mock_driver)

        self.assertFalse(mock_driver.door_signal)
        self.assertEqual(door_model.state.__class__.__name__, "ClosingState")

        LOGGER.debug("The lower switch closed")
        mock_driver.lower_limit_switch = True
        signal(SIGNAL_LOWER_SWITCH_CHANGED).send(mock_driver)

        self.assertEqual(door_model.state.__class__.__name__, "ClosedState")
        self.assertEqual(door_model.intent, IDLE_INTENT)

    def test_state_opening(self):
        """Test a walk from opening to closed."""

        # Door is opening
        mock_driver = MockDriver()
        door_model = Door("Test door", mock_driver, 1, 0.1, 0.3)
        door_model.set_new_state("Opening")

        # start intent
        door_model.set_intent(CLOSE_INTENT)

        # Door should be triggered to stop
        self.assertEqual(mock_driver.trigger_count, 0, "Nothing should be triggerd")
        time.sleep(0.2)
        self.assertEqual(mock_driver.trigger_count, 1, "First trigger to stop the door")

        # Door should be triggered again to start moving up
        time.sleep(0.3)
        self.assertEqual(mock_driver.trigger_count, 2, "Second trigger to start door moving up")

        # After moving, the upper switch closes
        time.sleep(0.5)
        mock_driver.lower_limit_switch = True
        signal(SIGNAL_LOWER_SWITCH_CHANGED).send(mock_driver)
        self.assertEqual(door_model.state.__class__.__name__, "ClosedState")
        self.assertEqual(door_model.intent, IDLE_INTENT)
        self.assertEqual(mock_driver.trigger_count, 2, "No additional triggers allowed")
