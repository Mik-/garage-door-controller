""" This module provides the error state and a factory for it."""

import logging
from .state import State

LOGGER = logging.getLogger('garage.door.' + __name__)

class ErrorState(State):
    """This class represents the intermediate state."""

    def __init__(self, door_model):
        super(ErrorState, self).__init__()

        self.door_model = door_model

    def door_position_changed(self, new_position):
        """This method is called by the door model, when its positions is changed."""
        LOGGER.debug("Door position changed in state 'error'")

    def enter(self):
        """This method is called by the door model, if this state is entered."""
        LOGGER.debug("State 'error' entered")

    def exit(self):
        """This method is called by the door model, if this state is exited."""
        LOGGER.debug("State 'error' exited")

class ErrorStateFactory(object):
    """This factory creates an ErrorState instance."""

    @staticmethod
    def create_state(door_model):
        """This method creates an ErrorState instance.

        Args:
            door_model: The door model to assign.
        """

        # Create a new instance
        instance = ErrorState(door_model)

        # There are no actions to register in this state

        return instance
