"""This module provides the delay command class."""

from threading import Timer

class DelayCommand(object):
    """This command performs a delay."""

    def __init__(self, delay_time):
        self.door = None
        self.timer = None
        self.delay_time = delay_time

    def execute(self, door):
        """This method will be called by the model, to execute this command."""
        self.door = door
        self.timer = Timer(self.delay_time, self._timeout)
        self.timer.start()
    
    def cancel(self):
        """This method will be called, to cancel the delay."""
        if self.timer is not None:
            self.timer.cancel()
            self.timer = None

    def _timeout(self):
        self.timer = None
        self.door.command_done()

