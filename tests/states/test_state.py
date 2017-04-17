"""This module provides a tests for the State class."""

import unittest
from garage.door.states.state import State

class ConcreteState(State):
    """An concrete implementation to test an abstract class."""

    def __init__(self):
        State.__init__(self)

    def door_position_changed(self, new_position):
        """Do nothing."""
        pass

    def enter(self):
        """Do nothing."""
        pass

    def exit(self):
        """Do nothing."""
        pass

class TestState(unittest.TestCase):
    """This class tests the State class."""

    def test_actions_dictionary(self):
        """This method tests the actions dictionary."""

        state = ConcreteState()

        state.register_action('test1', lambda: "test 1")
        state.register_action('test2', lambda: "test 2")

        self.assertEqual(state.get_action('test1')(), "test 1")
        self.assertEqual(state.get_action('test2')(), "test 2")

        nope = state.get_action('test3')
        self.assertIsNone(nope, "Test 3 should be not defined")
