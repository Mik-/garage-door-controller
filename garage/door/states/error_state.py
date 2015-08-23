import logging

logger = logging.getLogger(__name__)

class ErrorState:
    def __init__(self, door_model):
        self.door_model = door_model

    def enter(self):
        logger.error("State 'error' entered")

    def exit(self):
        logger.debug("State 'error' exited")
