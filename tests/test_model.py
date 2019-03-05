"""This module provides tests to the model class."""

import unittest
from mock import Mock
from garage.door.driver import Driver
from garage.door.model import Door
from garage.door.intents import OPEN_INTENT
from garage.door.states.state import State
from garage.door.commands.nop import NopCommand

class TestModel(unittest.TestCase):
    """This class test the door model."""

    def test_queue_state_commands(self):
        """Test the queue_state_commands method."""

        mock_driver = Mock(Driver)
        door = Door("Door 1", mock_driver, 1, 0.1, 0.3)

        state = Mock(State)
        door.state = state

        door.queue_state_commands(OPEN_INTENT)

        state.get_action.assert_called_with(OPEN_INTENT)

    def test_invoke_next_command_1(self):
        """Test the invoke_next_command method with an empty queue."""

        mock_driver = Mock(Driver)
        door = Door("Door 1", mock_driver, 1, 0.1, 0.3)

        state = Mock(State)
        door.state = state
        door.intent = OPEN_INTENT

        door.invoke_next_command()

        state.get_action.assert_called_with(OPEN_INTENT)
        self.assertIsNone(door.running_command, "Running command should be None")

    def test_invoke_next_command_2(self):
        """Test the invoke_next_command method with a nop command in queue."""

        mock_driver = Mock(Driver)
        door = Door("Door 1", mock_driver, 1, 0.1, 0.3)

        command = Mock(NopCommand)
        door.command_queue.put(command)

        door.invoke_next_command()

        command.execute.assert_called_once_with(door)
        self.assertEqual(door.running_command, command, "Running command should be assigned")

    def test_command_done(self):
        """Test the command_done method."""

        mock_driver = Mock(Driver)
        door = Door("Door 1", mock_driver, 1, 0.1, 0.3)

        command = Mock(NopCommand)
        door.running_command = command

        state = Mock(State)
        door.state = state
        door.intent = OPEN_INTENT

        door.command_done()

        state.get_action.assert_called_once_with(OPEN_INTENT)
        self.assertIsNone(door.running_command, "Running command should be None")

    def test_reset_command_queue(self):
        """Test the reset_command_queue method."""

        mock_driver = Mock(Driver)
        door = Door("Door 1", mock_driver, 1, 0.1, 0.3)

        running_command = Mock(NopCommand)
        door.running_command = running_command

        queued_command = Mock(NopCommand)
        door.command_queue.put(queued_command)

        door.reset_command_queue()

        running_command.execute.assert_not_called()
        running_command.cancel.assert_called_once()
        queued_command.execute.assert_not_called()
        queued_command.cancel.assert_not_called()
        self.assertTrue(door.command_queue.empty(), "Command queue should be empty")

if __name__ == '__main__':
    unittest.main()
