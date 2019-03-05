"""
Test a complete walk of a perfect door.
"""

import unittest
import time
from garage.door.model import Door
from garage.door.intents import IDLE_INTENT, OPEN_INTENT, CLOSE_INTENT
from perfect_door_driver import PerfectDoorDriver

class TestPerfectDoor(unittest.TestCase):
    """
    Test a walk of a perfect door.
    """

    def test_perfect_door(self):
        """
        Test a walk of a perfect door.
        """

        # Door is closed
        driver = PerfectDoorDriver(0.4, 0.15)
        door_model = Door("Test door", driver, 0.5, 0.1, 0.2)

        # The door is closed and idle
        self.assertEqual(door_model.state.__class__.__name__, 'ClosedState')
        self.assertEqual(door_model.intent, IDLE_INTENT)
        # Set "open" intent
        door_model.set_intent(OPEN_INTENT)
        self.assertEqual(door_model.intent, OPEN_INTENT)
        self.assertTrue(driver.door_signal)
        time.sleep(0.2)
        # After 0.15 seconds, the door should be in transit to upper position
        self.assertFalse(driver.door_signal)
        self.assertEqual(door_model.state.__class__.__name__, 'OpeningState')
        self.assertEqual(door_model.intent, OPEN_INTENT)
        self.assertFalse(driver.lower_limit_switch)
        self.assertFalse(driver.upper_limit_switch)
        time.sleep(0.25)
        # After 0.4 seconds, the door should be in upper position
        self.assertEqual(door_model.state.__class__.__name__, 'OpenState')
        self.assertEqual(door_model.intent, IDLE_INTENT)
        self.assertTrue(driver.upper_limit_switch)

        # The door is open and idle
        # Set "close" intent
        door_model.set_intent(CLOSE_INTENT)
        self.assertEqual(door_model.intent, CLOSE_INTENT)
        self.assertTrue(driver.door_signal)
        time.sleep(0.2)
        # After 0.15 seconds, the door should be in transit to lower position
        self.assertFalse(driver.door_signal)
        self.assertEqual(door_model.state.__class__.__name__, 'ClosingState')
        self.assertEqual(door_model.intent, CLOSE_INTENT)
        self.assertFalse(driver.lower_limit_switch)
        self.assertFalse(driver.upper_limit_switch)
        time.sleep(0.25)
        # After 0.4 seconds, the door should be in lower position
        self.assertEqual(door_model.state.__class__.__name__, 'ClosedState')
        self.assertEqual(door_model.intent, IDLE_INTENT)
        self.assertTrue(driver.lower_limit_switch)
