from ..positions import *

class OpeningState:
    def __init__(self, door_model):
        self.door_model = door_model

    def door_position_changed(self, new_position):
        if new_position == DOOR_POSITION_OPEN:
            self.door_model.set_new_state("Open")
        elif new_position == DOOR_POSITION_CLOSED:
            self.door_model.set_new_state("Closed")

    def enter(self):
        # Start timer, after which the door has to be OpenState
        # If the timer expired, switch to state INTERMEDIATE
        pass

    def exit(self):
        pass
