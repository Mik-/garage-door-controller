""" This module provides the init state and a factory for it."""

import logging
from ..positions import DOOR_POSITION_INTERMEDIATE, DOOR_POSITION_CLOSED, DOOR_POSITION_OPEN
from .state import State

LOGGER = logging.getLogger('garage.door.' + __name__)

class InitState(State):
    """This class represents the init state."""

    def __init__(self, door_model):
        super(InitState, self).__init__()

        self.door_model = door_model

    def door_position_changed(self, new_position):
        """This method is called by the door model, when its positions is changed."""
        raise NotImplementedError


    def enter(self):
        """This method is called by the door model, if this state is entered."""

        LOGGER.debug("State 'init' entered")

        if self.door_model.get_door_position() == DOOR_POSITION_INTERMEDIATE:
            self.door_model.set_new_state("Intermediate")
        elif self.door_model.get_door_position() == DOOR_POSITION_CLOSED:
            self.door_model.set_new_state("Closed")
        elif self.door_model.get_door_position() == DOOR_POSITION_OPEN:
            self.door_model.set_new_state("Open")

    def exit(self):
        """This method is called by the door model, if this state is exited."""
        LOGGER.debug("State 'init' exited")

class InitStateFactory(object):
    """This factory creates a InitState instance."""

    @staticmethod
    def create_state(door_model):
        """This method creates a InitState instance.

        Args:
            door_model: The door model to assign.
        """

        # Create a new instance
        instance = InitState(door_model)

        # There are no actions to register in this state

        return instance
