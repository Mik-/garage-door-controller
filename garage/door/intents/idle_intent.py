import logging

class IdleIntent:
    def __init__(self, door_model):
        self.door_model = door_model

    def start(self):
        """This intent should do nothing."""
        pass

    def cleanup(self):
        """Nothing to clean up."""
        pass
