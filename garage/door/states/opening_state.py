from threading import Timer
from ..positions import *
import logging

logger = logging.getLogger('garage.door.' + __name__)

class OpeningState:
    def __init__(self, door_model):
        self.door_model = door_model

    def door_position_changed(self, new_position):
        if new_position == DOOR_POSITION_OPEN:
            self.door_model.set_new_state("Open")
        elif new_position == DOOR_POSITION_CLOSED:
            self.door_model.set_new_state("Closed")

    def enter(self):
        logger.debug("State 'opening' entered")
        self.timer = Timer(self.door_model.transit_time, self._transit_timeout)
        self.timer.start()

    def exit(self):
        logger.debug("State 'opening' exited")
        if self.timer:
            self.timer.cancel()
            self.timer = False

    def _transit_timeout(self):
        logger.info("Transit timeout reached")
        self.timer = False
        self.door_model.set_new_state("Intermediate")
