"""
Test a door, which stuck somewhere.
"""

import unittest
import time
from garage.door.model import Door
from garage.door.intents import IDLE_INTENT, CLOSE_INTENT, OPEN_INTENT
from stuck_door_driver import StuckDoorDriver

class TestStuckDoor(unittest.TestCase):
    """
    Test a door, which stuck somewhere.
    """
    def test_stuck_door(self):
        """
        Test a door, which stuck somewhere.
        """

        # Door is closed
        driver = StuckDoorDriver(0.4, 0.15)
        door_model = Door("Test door", driver, 0.5, 0.1, 0.2)

        # The door is closed and idle
        self.assertEqual(door_model.state.__class__.__name__, 'ClosedState')
        self.assertEqual(door_model.intent, IDLE_INTENT)
        # Set "open" intent
        door_model.set_intent(OPEN_INTENT)
        self.assertEqual(door_model.intent, OPEN_INTENT)
        self.assertTrue(driver.door_signal)
        time.sleep(0.175)
        # After 0.15 seconds, the door stucks in lower position
        self.assertFalse(driver.door_signal)
        self.assertEqual(door_model.state.__class__.__name__, 'ClosedState')
        self.assertEqual(door_model.intent, OPEN_INTENT)
        self.assertTrue(driver.lower_limit_switch)
        self.assertFalse(driver.upper_limit_switch)
        time.sleep(0.05)
        # After 0.2 seconds, the door should be triggered once more
        self.assertTrue(driver.door_signal)
        time.sleep(0.2)
        # After 0.4 seconds, the door should be in transit to upper position
        self.assertFalse(driver.door_signal)
        self.assertEqual(door_model.state.__class__.__name__, 'OpeningState')
        self.assertEqual(door_model.intent, OPEN_INTENT)
        self.assertFalse(driver.lower_limit_switch)
        self.assertFalse(driver.upper_limit_switch)
