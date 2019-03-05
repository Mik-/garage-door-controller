""" This module provides the opening state and a factory for it."""

import logging
from threading import Timer
from ..positions import DOOR_POSITION_CLOSED, DOOR_POSITION_OPEN
from .state import State
from garage.door.commands.delay import DelayCommand
from garage.door.commands.trigger_door import TriggerDoorCommand
from garage.door.intents import OPEN_INTENT, CLOSE_INTENT

LOGGER = logging.getLogger('garage.door.' + __name__)

class OpeningState(State):
    """This class represents the intermediate state."""

    def __init__(self, door_model):
        super(OpeningState, self).__init__()

        self.door_model = door_model
        self.timer = None

    def door_position_changed(self, new_position):
        """This method is called by the door model, when its positions is changed."""

        if new_position == DOOR_POSITION_OPEN:
            self.door_model.set_new_state("Open")
        elif new_position == DOOR_POSITION_CLOSED:
            self.door_model.set_new_state("Closed")

    def enter(self):
        """This method is called by the door model, if this state is entered."""
        LOGGER.debug("State 'opening' entered")
        self.timer = Timer(self.door_model.transit_time, self._transit_timeout)
        self.timer.start()

    def exit(self):
        """This method is called by the door model, if this state is exited."""
        LOGGER.debug("State 'opening' exited")
        if self.timer is not None:
            self.timer.cancel()
            self.timer = None

    def _transit_timeout(self):
        LOGGER.info("Transit timeout reached")
        self.timer = None
        self.door_model.set_new_state("Intermediate")

class OpeningStateFactory(object):
    """This factory creates an OpeningState instance."""

    @staticmethod
    def create_state(door_model):
        """This method creates an OpeningState instance.

        Args:
            door_model: The door model to assign.
        """

        # Create a new instance
        instance = OpeningState(door_model)

        # Register commands for the open intent
        def queue_open_intent_commands(door):
            """This method add commands for the open intent to the door command queue."""
            door.command_queue.put(DelayCommand(door_model.transit_time))

        instance.register_action(OPEN_INTENT, queue_open_intent_commands)

        # Register command for the close intent
        def queue_close_intent_commands(door):
            """This method add commands for the close intent to the door command queue."""
            door.command_queue.put(TriggerDoorCommand())
            door.command_queue.put(DelayCommand(door_model.accelerate_time))
            door.command_queue.put(TriggerDoorCommand())
            door.command_queue.put(DelayCommand(door_model.transit_time))

        instance.register_action(CLOSE_INTENT, queue_close_intent_commands)

        return instance
