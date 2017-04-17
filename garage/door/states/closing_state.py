""" This module provides the closing state and a factory for it."""

import logging
from threading import Timer
from ..positions import DOOR_POSITION_CLOSED, DOOR_POSITION_OPEN
from .state import State

LOGGER = logging.getLogger('garage.door.' + __name__)

class ClosingState(State):
    """This class represents the closing state."""

    def __init__(self, door_model):
        super(ClosingState, self).__init__()

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
        LOGGER.debug("State 'closing' entered")

        self.timer = Timer(self.door_model.transit_time, self._transit_timeout)
        self.timer.start()

    def exit(self):
        """This method is called by the door model, if this state is exited."""
        LOGGER.debug("State 'closing' exited")

        if self.timer is not None:
            self.timer.cancel()
            self.timer = None

    def _transit_timeout(self):
        LOGGER.info("Transit timeout reached.")

        self.timer = None
        self.door_model.set_new_state("Intermediate")

class ClosingStateFactory(object):
    """This factory creates a ClosingState instance."""

    @staticmethod
    def create_state(door_model):
        """This method creates a ClosingState instance.

        Args:
            door_model: The door model to assign.
        """

        # Create a new instance
        instance = ClosingState(door_model)

        # There are no actions to register in this state

        return instance
