"""This module provides the nop command class."""

class NopCommand(object):
    """This command does nothing."""

    def execute(self, door):
        """This method will be called by the model, to execute this command."""
        door.command_done()

    def cancel(self):
        """This method will be called, to cancel this command."""
        pass
