import logging

class ErrorState:
    def __init__(self, door_model):
        self.door_model = door_model

    def enter(self):
        logging.error("State 'error' entered")

    def exit(self):
        logging.error("State 'error' exited")
