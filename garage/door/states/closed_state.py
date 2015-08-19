from ..positions import *
import logging

class ClosedState:
    def __init__(self, door_model):
        self.door_model = door_model

    def door_position_changed(self, new_position):
        if new_position == DOOR_POSITION_OPEN:
            self.door_model.set_new_state("Open")
        elif new_position == DOOR_POSITION_INTERMEDIATE:
            self.door_model.set_new_state("Opening")

    def enter(self):
        logging.debug("State 'closed' entered")

    def exit(self):
        logging.debug("State 'closed' exited")
        self.door_model.stop_door_signal()
