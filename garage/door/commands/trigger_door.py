"""This module provides the trigger door command class."""

from threading import Timer

class TriggerDoorCommand(object):
    """This command triggers the door."""

    def __init__(self):
        self.door = None
        self.timer = None

    def execute(self, door):
        """This method will be called by the model, to execute this command."""
        self.door = door
        self.door.start_door_signal()
        self.timer = Timer(self.door.trigger_time, self._timeout)
        self.timer.start()

    def cancel(self):
        """This method will be called, to cancel the door trigger."""
        if self.timer is not None:
            self.timer.cancel()
            self.timer = None

            self.door.stop_door_signal()

    def _timeout(self):
        self.timer = None
        self.door.stop_door_signal()
        self.door.command_done()

