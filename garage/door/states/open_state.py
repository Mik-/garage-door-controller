""" This module provides the open state and a factory for it."""

import logging
from ..positions import DOOR_POSITION_CLOSED, DOOR_POSITION_INTERMEDIATE
from .state import State
from garage.door.commands.set_intent import SetIntentCommand
from garage.door.commands.delay import DelayCommand
from garage.door.commands.trigger_door import TriggerDoorCommand
from garage.door.intents import IDLE_INTENT, OPEN_INTENT, CLOSE_INTENT

LOGGER = logging.getLogger('garage.door.' + __name__)

class OpenState(State):
    """This class represents the open state."""

    def __init__(self, door_model):
        super(OpenState, self).__init__()

        self.door_model = door_model

    def door_position_changed(self, new_position):
        """This method is called by the door model, when its positions is changed."""

        if new_position == DOOR_POSITION_CLOSED:
            self.door_model.set_new_state("Closed")
        elif new_position == DOOR_POSITION_INTERMEDIATE:
            self.door_model.set_new_state("Closing")

    def enter(self):
        """This method is called by the door model, if this state is entered."""
        LOGGER.debug("State 'open' entered")

    def exit(self):
        """This method is called by the door model, if this state is exited."""
        LOGGER.debug("State 'open' exited")
        self.door_model.stop_door_signal()

class OpenStateFactory(object):
    """This factory creates an OpenState instance."""

    @staticmethod
    def create_state(door_model):
        """This method creates an OpenState instance.

        Args:
            door_model: The door model to assign.
        """

        # Create a new instance
        instance = OpenState(door_model)

        # Register command for the open intent
        def queue_open_intent_commands(door):
            """This method add commands for the open intent to the door command queue."""
            door.command_queue.put(SetIntentCommand(IDLE_INTENT))

        instance.register_action(OPEN_INTENT, queue_open_intent_commands)

        # Register command sfor the close intent
        def queue_close_intent_commands(door):
            """This method add commands for the close intent to the door command queue."""
            door.command_queue.put(DelayCommand(door_model.accelerate_time))
            door.command_queue.put(TriggerDoorCommand())

        instance.register_action(CLOSE_INTENT, queue_close_intent_commands)

        return instance
