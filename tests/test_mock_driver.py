"""This modules provides the MockDriverTest class."""

import unittest
from tests.mock_driver import MockDriver

class TestMockDriver(unittest.TestCase):
    """This class tests the mock driver."""

    def test_trigger_count(self):
        """Test the trigger count."""

        mock_driver = MockDriver()
        self.assertEqual(mock_driver.trigger_count, 0)

        mock_driver.start_door_signal()
        self.assertEqual(mock_driver.trigger_count, 0)

        mock_driver.stop_door_signal()
        self.assertEqual(mock_driver.trigger_count, 1)

        mock_driver.start_door_signal()
        self.assertEqual(mock_driver.trigger_count, 1)

        mock_driver.stop_door_signal()
        self.assertEqual(mock_driver.trigger_count, 2)

        mock_driver.start_door_signal()
        self.assertEqual(mock_driver.trigger_count, 2)

        mock_driver.stop_door_signal()
        self.assertEqual(mock_driver.trigger_count, 3)
