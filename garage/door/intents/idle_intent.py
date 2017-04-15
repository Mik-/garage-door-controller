"""This module provides the IdleIntent class."""

class IdleIntent(object):
    """This class represents the idle intent. No door controlling is done."""

    def __init__(self, door_model):
        self.door_model = door_model

    def start(self):
        """This initialized the intent."""
        pass

    def cleanup(self):
        """Cleanup things."""
        pass
