""" This module provides the ClosedState class."""

import logging
from ..positions import DOOR_POSITION_INTERMEDIATE, DOOR_POSITION_OPEN

LOGGER = logging.getLogger('garage.door.' + __name__)

class ClosedState:
    """This class reperesent the state of a closed door and handles 
    the events accordingly."""

    def __init__(self, door_model):
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
        LOGGER.debug("State 'closed' entered")

    def exit(self):
        LOGGER.debug("State 'closed' exited")
        self.door_model.stop_door_signal()
