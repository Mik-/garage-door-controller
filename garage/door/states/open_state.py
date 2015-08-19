from ..positions import *
import logging

class OpenState:
    def __init__(self, door_model):
        self.door_model = door_model

    def door_position_changed(self, new_position):
        if new_position == DOOR_POSITION_CLOSED:
            self.door_model.set_new_state("Closed")
        elif new_position == DOOR_POSITION_INTERMEDIATE:
            self.door_model.set_new_state("Closing")

    def enter(self):
        logging.error("State 'open' entered")

    def exit(self):
        logging.error("State 'open' exited")
        self.door_model.stop_door_signal()
