"""This module provides the set intent command class."""

class SetIntentCommand(object):
    """This command sets a new intent."""

    def __init__(self, intent):
        self.new_intent = intent

    def execute(self, door):
        """This method will be called by the model, to execute this command."""
        door.set_intent(self.new_intent)
        door.command_done()

    def cancel(self):
        """This method will be called, to cancel new intent."""
        pass
