"""This module provides the Door class."""

import logging
from Queue import Queue, Empty
from blinker import signal
from garage.door.signals import SIGNAL_LOWER_SWITCH_CHANGED, SIGNAL_UPPER_SWITCH_CHANGED
from garage.door.signals import SIGNAL_DOOR_STATE_CHANGED
from garage.door.positions import DOOR_POSITION_CLOSED, DOOR_POSITION_ERROR
from garage.door.positions import DOOR_POSITION_INTERMEDIATE, DOOR_POSITION_OPEN
from garage.door.states.state import StateFactory
from garage.door.intents import IDLE_INTENT

LOGGER = logging.getLogger('garage.door.' + __name__)

class Door(object):
    """This class builds the representation of a door.
    """

    def __init__(self, name, driver, transit_time, trigger_time, accelerate_time):
        LOGGER.debug("Door '%s' instantiation start", name)

        self.command_queue = Queue()
        self.running_command = None

        self.name = name
        self.driver = driver
        self.intent = IDLE_INTENT
        self.state = None
        if self._check_for_error_condition():
            self.set_new_state("Error")
        else:
            self.set_new_state("Init")
        self.transit_time = transit_time     # time, the door need for opening or closing
        self.trigger_time = trigger_time     # time, the relais will triggered to move door
        # time, the door need to move out of switch position, after the engine is triggerd
        self.accelerate_time = accelerate_time
        signal(SIGNAL_LOWER_SWITCH_CHANGED).connect(self._switch_changed, sender=self.driver)
        signal(SIGNAL_UPPER_SWITCH_CHANGED).connect(self._switch_changed, sender=self.driver)

        LOGGER.debug("Door '%s' instantiated", name)

    def cleanup(self):
        """Cleanup object, i.e. disconnnect from signals and so on."""
        LOGGER.debug('Model cleanup.')
        signal(SIGNAL_LOWER_SWITCH_CHANGED).disconnect(self._switch_changed)
        signal(SIGNAL_UPPER_SWITCH_CHANGED).disconnect(self._switch_changed)

        self.reset_command_queue()

        self.stop_door_signal()

        self.driver.cleanup()

    def start_door_signal(self):
        """Triggers the physical door controller by closing the relay.
        The relay will be openend after the specified trigger_time or by a
        call to stop_door_signal."""
        LOGGER.debug("Start door signal")
        self.driver.start_door_signal()

    def stop_door_signal(self):
        """Closes the relay, which triggers the physical door controller."""
        LOGGER.debug("Stop door signal")
        self.driver.stop_door_signal()

    def set_new_state(self, new_state_name):
        """Set the new controller state."""

        # Cancel the running command and clear the command queue
        self.reset_command_queue()

        # If a state is assigned, call the exit method. On the first call of
        # this method, there is no state assigned
        if self.state is not None:
            self.state.exit()

        # Get a new state instance
        self.state = StateFactory.create_state(new_state_name, self)

        self.state.enter()

        # Call the next command, to fulfill the desired intent
        # If no commands are queued, the commands defined by the state
        # will be queued first.
        self.invoke_next_command()

        signal(SIGNAL_DOOR_STATE_CHANGED).send(self)

    def get_door_position(self):
        """Returns the current door position, which is determined by the
        state of the limit switches."""
        if not self.driver.get_lower_limit_switch_state() and \
            not self.driver.get_upper_limit_switch_state():
            return DOOR_POSITION_INTERMEDIATE
        elif self.driver.get_lower_limit_switch_state() and \
            not self.driver.get_upper_limit_switch_state():
            return DOOR_POSITION_CLOSED
        elif not self.driver.get_lower_limit_switch_state() and \
            self.driver.get_upper_limit_switch_state():
            return DOOR_POSITION_OPEN
        else:
            return DOOR_POSITION_ERROR

    def _switch_changed(self, sender):
        """Callback method, which is called by the driver by emitting a certain
        signal."""
        LOGGER.debug("Limit switches have changed their state to %d", self.get_door_position())

        if not self._check_for_error_condition():
            self.state.door_position_changed(self.get_door_position())

    def _check_for_error_condition(self):
        """If the limit switches report a error state, I detect it here, so I
        don't have to check it in every state class."""
        if self.get_door_position() == DOOR_POSITION_ERROR:
            self.set_new_state("Error")
            return True
        else:
            return False

    def set_intent(self, new_intent):
        """Set the new intent."""

        LOGGER.debug("Setting new intent: %d", new_intent)

        if self.intent != new_intent:
            # stop running commands
            self.reset_command_queue()

            self.intent = new_intent

            self.invoke_next_command()

    def invoke_next_command(self):
        """Calls the next queue command, if any is available."""

        try:
            # If queue is empty, add commands from current state
            if self.command_queue.empty():
                self.queue_state_commands(self.intent)

            # Execute the next command in queue
            if not self.command_queue.empty():
                self.running_command = self.command_queue.get_nowait()
                self.running_command.execute(self)
        except Empty:
            pass

    def command_done(self):
        """This method should be called by every command, when it's action is done."""
        self.running_command = None
        self.invoke_next_command()

    def reset_command_queue(self):
        """This method cancels the running command and clears the command queue."""
        # Cancel the running command
        if self.running_command is not None:
            self.running_command.cancel()
            self.running_command = None

        # Create a new command queue -> clear current queue
        self.command_queue = Queue()

    def queue_state_commands(self, intent):
        """This method fills the command queue with the command, defined by the
        current state for the given intent."""

        state_action = self.state.get_action(intent)
        if state_action is not None:
            state_action(self)
