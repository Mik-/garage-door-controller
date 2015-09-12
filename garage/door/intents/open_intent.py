from ..signals import *
from blinker import signal
from threading import Timer
import logging

logger = logging.getLogger('garage.door.' + __name__)

class OpenIntent:
    def __init__(self, door_model):
        self.door_model = door_model
        self.timer = False

    def start(self):
        """This intent controls the model in that way, that the door is
        eventually open."""
        logger.debug("Intent 'Open' started.")
        self.allowed_state_changes = 5

        signal(SIGNAL_DOOR_STATE_CHANGED).connect(self._state_changed, sender=self.door_model)

        self._send_command_to_door()

    def cleanup(self):
        """Do cleanup tasks. Disconnect from signals an so on."""
        logger.debug("Cleanup intent " + self.__class__.__name__)

        if self.timer:
            self.timer.cancel()
            self.timer = False
            
        signal(SIGNAL_DOOR_STATE_CHANGED).disconnect(self._state_changed, sender=self.door_model)

    def _state_changed(self, sender):
        self.allowed_state_changes -= 1
        if self.allowed_state_changes <= 0:
            # Too many state changes, stop this intent
            logger.warning("Intent 'Open' aborted due to many state changes!")
            self.door_model.set_intent("Idle")
        elif sender == self.door_model:
            self._send_command_to_door()
        else:
            logger.debug("This intent don't handle door %s.", sender.__class__.__name__)


    def _send_command_to_door(self):
        if self.timer:
            self.timer.cancel()

        if self.door_model.state.__class__.__name__ == "OpenState":
            # The intent is fulfilled
            logger.debug("Intent 'Open' fulfilled.")
            self.door_model.set_intent("Idle")

        elif self.door_model.state.__class__.__name__ == "ClosedState":
            # The door is closed. Trigger the door to open it
            logger.debug("Door is closed. Trigger opening.")
            self.door_model.start_door_signal()
            self._set_timer(self.door_model.accelerate_time)

        elif self.door_model.state.__class__.__name__ == "OpeningState":
            # The door is going to be open. Just wait
            logger.debug("Waiting.")
            self._set_timer(self.door_model.transit_time)

        elif self.door_model.state.__class__.__name__ == "ClosingState":
            # The door is going to be closed. Stop it, wait and open it
            logger.debug("Stop door to open it with the next command.")
            self.door_model.start_door_signal()
            self._set_timer(self.door_model.transit_time)

        elif self.door_model.state.__class__.__name__ == "IntermediateState":
            logger.debug("Start door and wait for the next state.")
            self.door_model.start_door_signal()
            self._set_timer(self.door_model.transit_time)

        elif self.door_model.state.__class__.__name__ == "ErrorState":
            logger.debug("Door in error state. Abort intent.")
            self.door_model.set_intent("Idle")
        else:
            logger.error("Unhandled door state %s", self.door_model.state.__class__.__name__)
            self.door_model.set_intent("Idle")

    def _set_timer(self, time):
            if self.timer:
                self.timer.cancel()
            self.timer = Timer(time, self._timeout)
            self.timer.start()

    def _timeout(self):
        logger.debug("Timeout occured.")
        self._state_changed(self.door_model)
