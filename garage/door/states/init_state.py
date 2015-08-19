from ..positions import *
import logging

class InitState:
    def __init__(self, door_model):
        self.door_model = door_model

    def enter(self):
        logging.error("State 'init' entered")

        if self.door_model.get_door_position() == DOOR_POSITION_INTERMEDIATE:
            self.door_model.set_new_state("Intermediate")
        elif self.door_model.get_door_position() == DOOR_POSITION_CLOSED:
            self.door_model.set_new_state("Closed")
        elif self.door_model.get_door_position() == DOOR_POSITION_OPEN:
            self.door_model.set_new_state("Open")

    def exit(self):
        logging.error("State 'init' exited")
