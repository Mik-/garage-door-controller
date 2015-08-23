from ..positions import *
import logging

logger = logging.getLogger(__name__)

class IntermediateState:
    def __init__(self, door_model):
        self.door_model = door_model

    def door_position_changed(self, new_position):
        if new_position == DOOR_POSITION_OPEN:
            self.door_model.set_new_state("Open")
        elif new_position == DOOR_POSITION_CLOSED:
            self.door_model.set_new_state("Closed")

    def enter(self):
        logger.debug("State 'intermediate' entered")

    def exit(self):
        logger.debug("State 'intermediate' exited")
