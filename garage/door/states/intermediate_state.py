""" This module provides the intermediate state and a factory for it."""

import logging
from ..positions import DOOR_POSITION_CLOSED, DOOR_POSITION_OPEN
from .state import State

LOGGER = logging.getLogger('garage.door.' + __name__)

class IntermediateState(State):
    """This class represents the intermediate state."""

    def __init__(self, door_model):
        super(IntermediateState, self).__init__()

        self.door_model = door_model

    def door_position_changed(self, new_position):
        """This method is called by the door model, when its positions is changed."""

        if new_position == DOOR_POSITION_OPEN:
            self.door_model.set_new_state("Open")
        elif new_position == DOOR_POSITION_CLOSED:
            self.door_model.set_new_state("Closed")

    def enter(self):
        """This method is called by the door model, if this state is entered."""
        LOGGER.debug("State 'intermediate' entered")

    def exit(self):
        """This method is called by the door model, if this state is exited."""
        LOGGER.debug("State 'intermediate' exited")

class IntermediateStateFactory(object):
    """This factory creates an IntermediateState instance."""

    @staticmethod
    def create_state(door_model):
        """This method creates an IntermediateState instance.

        Args:
            door_model: The door model to assign.
        """

        # Create a new instance
        instance = IntermediateState(door_model)

        # There are no actions to register in this state

        return instance
