"""This module provides the CloseIntent class."""

import logging
from threading import Timer
from blinker import signal
from ..signals import SIGNAL_DOOR_STATE_CHANGED

LOGGER = logging.getLogger('garage.door.' + __name__)
MAX_STATE_CHANGES = 8

class CloseIntent(object):
    """This class implements the close intent.

    This intent controls the model in that way, that the door is
    eventually closed."""

    def __init__(self, door_model):
        self.door_model = door_model
        self.timer = False
        self.allowed_state_changes = 0
        self.last_state_name = ""

    def start(self):
        """Initialize the intent and call the actions to close the door."""

        LOGGER.debug("Intent 'Close' started.")
        self.allowed_state_changes = MAX_STATE_CHANGES

        self.last_state_name = self.door_model.state.__class__.__name__

        signal(SIGNAL_DOOR_STATE_CHANGED).connect(self._state_changed, sender=self.door_model)

        self._send_command_to_door()

    def cleanup(self):
        """Do cleanup tasks. Disconnect from signals an so on."""
        LOGGER.debug("Cleanup intent " + self.__class__.__name__)

        if self.timer:
            self.timer.cancel()
            self.timer = False

        signal(SIGNAL_DOOR_STATE_CHANGED).disconnect(self._state_changed, sender=self.door_model)

    def _state_changed(self, sender):
        """Handle the "state changed" event."""

        self.allowed_state_changes -= 1
        if self.allowed_state_changes <= 0:
            # Too many state changes, stop this intent
            LOGGER.warning("Intent 'Close' aborted due to many state changes!")
            self.door_model.set_intent("Idle")
        elif sender == self.door_model:
            self._send_command_to_door()
        else:
            LOGGER.debug("This intent don't handle door %s.", sender.__class__.__name__)


    def _send_command_to_door(self):
        if self.timer:
            self.timer.cancel()

        if self.door_model.state.__class__.__name__ == "ClosedState":
            # The intent is fulfilled
            LOGGER.debug("Intent 'Close' fulfilled.")
            self.door_model.set_intent("Idle")

        elif self.door_model.state.__class__.__name__ == "OpenState":
            # If the last state wasn't "open" just wait another accelerate time
            # to prevent direct triggering when the door is just moved into limit switch
            # After a wait time, this method is called again and the last state
            # is the same
            if self.last_state_name == 'OpenState':
                # The door is still open. Trigger the door to close it
                LOGGER.debug("Door is open. Trigger closing.")
                self.door_model.start_door_signal()

            self._set_timer(self.door_model.accelerate_time)

        elif self.door_model.state.__class__.__name__ == "ClosingState":
            # The door is going to be closed. Just wait
            LOGGER.debug("Waiting.")
            self._set_timer(self.door_model.transit_time)

        elif self.door_model.state.__class__.__name__ == "OpeningState":
            # The door is going to be open. Stop it, wait and close it
            LOGGER.debug("Stop door to close it with the next command.")
            self.door_model.start_door_signal()
            self._set_timer(self.door_model.accelerate_time)

        elif self.door_model.state.__class__.__name__ == "IntermediateState":
            LOGGER.debug("Start door and wait for the next state.")
            self.door_model.start_door_signal()
            self._set_timer(self.door_model.transit_time)

        elif self.door_model.state.__class__.__name__ == "ErrorState":
            LOGGER.debug("OpenIntent: Door in error state. Abort intent.")
            self.door_model.set_intent("Idle")
        else:
            LOGGER.error("Unhandled door state %s", self.door_model.state.__class__.__name__)
            self.door_model.set_intent("Idle")

        # remember the state to do something depending on it, when this method
        # is called the next time
        self.last_state_name = self.door_model.state.__class__.__name__

    def _set_timer(self, time):
        if self.timer:
            self.timer.cancel()
        self.timer = Timer(time, self._timeout)
        self.timer.start()

    def _timeout(self):
        LOGGER.debug("Timeout occured.")
        self._state_changed(self.door_model)
