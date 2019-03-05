""" This module provides the ClosedState class."""

import logging
from ..positions import DOOR_POSITION_INTERMEDIATE, DOOR_POSITION_OPEN
from .state import State
from garage.door.commands.set_intent import SetIntentCommand
from garage.door.commands.delay import DelayCommand
from garage.door.commands.trigger_door import TriggerDoorCommand
from garage.door.intents import IDLE_INTENT, OPEN_INTENT, CLOSE_INTENT

LOGGER = logging.getLogger('garage.door.' + __name__)

class ClosedState(State):
    """This class reperesent the state of a closed door and handles
    the events accordingly."""

    def __init__(self, door_model):
        super(ClosedState, self).__init__()

        self.door_model = door_model

    def door_position_changed(self, new_position):
        """Handles the door position changed event.

        Args:
            new_position (int): The new door position, which was triggering this event.
        """

        if new_position == DOOR_POSITION_OPEN:
            self.door_model.set_new_state("Open")
        elif new_position == DOOR_POSITION_INTERMEDIATE:
            self.door_model.set_new_state("Opening")

    def enter(self):
        """This method is called by the door model, if this state is entered."""
        LOGGER.debug("State 'closed' entered")

    def exit(self):
        """This method is called by the door model, if this state is exited."""
        LOGGER.debug("State 'closed' exited")
        self.door_model.stop_door_signal()

class ClosedStateFactory(object):
    """This factory creates a ClosedState instance."""

    @staticmethod
    def create_state(door_model):
        """This method creates a ClosedState instance.

        Args:
            door_model: The door model to assign.
        """

        # Create a new instance
        instance = ClosedState(door_model)

        # Register command for the open intent
        def queue_open_intent_commands(door):
            """This method add commands for the open intent to the door command queue."""
            # Try three times to start the door
            door.command_queue.put(DelayCommand(door_model.accelerate_time))
            door.command_queue.put(TriggerDoorCommand())
            door.command_queue.put(DelayCommand(door_model.accelerate_time))
            door.command_queue.put(TriggerDoorCommand())
            door.command_queue.put(DelayCommand(door_model.accelerate_time))
            door.command_queue.put(TriggerDoorCommand())

        instance.register_action(OPEN_INTENT, queue_open_intent_commands)

        # Register command sfor the close intent
        def queue_close_intent_commands(door):
            """This method add commands for the close intent to the door command queue."""
            door.command_queue.put(SetIntentCommand(IDLE_INTENT))

        instance.register_action(CLOSE_INTENT, queue_close_intent_commands)

        return instance
