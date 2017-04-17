"""This module provides the Door class."""

import logging
import importlib
from threading import Timer
from blinker import signal
from garage.door.signals import SIGNAL_LOWER_SWITCH_CHANGED, SIGNAL_UPPER_SWITCH_CHANGED
from garage.door.signals import SIGNAL_DOOR_STATE_CHANGED
from garage.door.positions import DOOR_POSITION_CLOSED, DOOR_POSITION_ERROR
from garage.door.positions import DOOR_POSITION_INTERMEDIATE, DOOR_POSITION_OPEN
from garage.door.states.state import StateFactory

LOGGER = logging.getLogger('garage.door.' + __name__)

class Door(object):
    """This class builds the representation of a door.
    """

    def __init__(self, name, driver, transit_time, trigger_time, accelerate_time):
        LOGGER.debug("Door '%s' instantiation start", name)

        self.name = name
        self.driver = driver
        self.trigger_timer = None
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

        self.intent = None
        self.set_intent("Idle")

        LOGGER.debug("Door '%s' instantiated", name)

    def cleanup(self):
        """Cleanup object, i.e. disconnnect from signals and so on."""
        LOGGER.debug('Model cleanup.')
        signal(SIGNAL_LOWER_SWITCH_CHANGED).disconnect(self._switch_changed)
        signal(SIGNAL_UPPER_SWITCH_CHANGED).disconnect(self._switch_changed)

        if self.trigger_timer is not None:
            self.trigger_timer.cancel()
            self.trigger_timer = None

        if self.intent is not None:
            self.intent.cleanup()
            self.intent = None

        self.driver.cleanup()

    def start_door_signal(self):
        """Triggers the physical door controller by closing the relay.
        The relay will be openend after the specified trigger_time or by a
        call to stop_door_signal."""
        LOGGER.debug("Start door signal")
        self.driver.start_door_signal()

        if self.trigger_timer is not None:
            self.trigger_timer.cancel()
        self.trigger_timer = Timer(self.trigger_time, self._trigger_timeout)
        self.trigger_timer.start()

    def stop_door_signal(self):
        """Closes the relay, which triggers the physical door controller."""
        LOGGER.debug("Stop door signal")

        self.driver.stop_door_signal()
        if self.trigger_timer is not None:
            self.trigger_timer.cancel()
            self.trigger_timer = None

    def set_new_state(self, new_state_name):
        """Set the new controller state."""
        # If a state is assigned, call the exit method. On the first call of
        # this method, there is no state assigned
        if self.state is not None:
            self.state.exit()
        
        # Get a new state instance
        self.state = StateFactory.create_state(new_state_name, self)

        self.state.enter()

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

    def _trigger_timeout(self):
        """The timeout for triggering the relay occured."""
        LOGGER.debug("Trigger timeout occured")
        self.trigger_timer = None
        self.stop_door_signal()

    def set_intent(self, new_intent_name):
        """Instantiate a new intent object by its name."""
        # Cleanup last intent
        if self.intent is not None:
            self.intent.cleanup()

        # Instantiate new intent
        LOGGER.debug("Setting new intent: " + new_intent_name)
        intent_module = importlib.import_module("garage.door.intents." +
                                                new_intent_name.lower() + "_intent")
        self.intent = getattr(intent_module, new_intent_name + "Intent")(self)

        self.intent.start()
