import logging

LOGGER = logging.getLogger('garage.door.' + __name__)

class ErrorState:
    def __init__(self, door_model):
        self.door_model = door_model

    def enter(self):
        LOGGER.debug("State 'error' entered")

    def exit(self):
        LOGGER.debug("State 'error' exited")
