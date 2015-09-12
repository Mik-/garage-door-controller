import importlib
from threading import Timer
from positions import *
from blinker import signal
from signals import *
import logging

logger = logging.getLogger('garage.door.' + __name__)

class Door(object):
    def __init__(self, name, driver, transit_time, trigger_time, accelerate_time):
        logger.debug("Door '%s' instantiation start", name)

        self.name = name
        self.driver = driver
        self.trigger_timer = False
        self.state = False # Init variable to prevent error on first call of set_new_state
        if self._check_for_error_condition() == True:
            self.set_new_state("Error")
        else:
            self.set_new_state("Init")
        self.transit_time = transit_time     # time, the door need for opening or closing
        self.trigger_time = trigger_time    # time, the relais will triggered to move door
        self.accelerate_time = accelerate_time    # time, the door need to move from switch, after the engine is triggerd
        signal(SIGNAL_LOWER_SWITCH_CHANGED).connect(self._switch_changed)
        signal(SIGNAL_UPPER_SWITCH_CHANGED).connect(self._switch_changed)

        self.intent = False
        self.set_intent("Idle")

        logger.debug("Door '%s' instantiated", name)

    def __del__(self):
        signal(SIGNAL_LOWER_SWITCH_CHANGED).disconnect(self._switch_changed)
        signal(SIGNAL_UPPER_SWITCH_CHANGED).disconnect(self._switch_changed)

    def start_door_signal(self):
        """Triggers the physical door controller by closing the relay.
        The relay will be openend after the specified trigger_time or by a
        call to stop_door_signal."""
        logger.debug("Start door signal")
        self.driver.start_door_signal()

        if self.trigger_timer:
            self.trigger_timer.cancel()
        self.trigger_timer = Timer(self.trigger_time, self._trigger_timeout)
        self.trigger_timer.start()

    def stop_door_signal(self):
        """Closes the relay, which triggers the physical door controller."""
        logger.debug("Stop door signal")

        self.driver.stop_door_signal()
        if self.trigger_timer:
            self.trigger_timer.cancel()
            self.trigger_timer = False

    def set_new_state(self, new_state_name):
        """Set the new controller state."""
        # If a state is assigned, call the exit method. On the first call of
        # this method, there is no state assigned
        if self.state:
            self.state.exit()
        # Instantiate a new state object by its name
        state_module = importlib.import_module("garage.door.states." + new_state_name.lower() + "_state")
        self.state = getattr(state_module, new_state_name + "State")(self)

        self.state.enter()

        signal(SIGNAL_DOOR_STATE_CHANGED).send(self)

    def get_door_position(self):
        """Returns the current door position, which is determined by the
        state of the limit switches."""
        if self.driver.get_lower_limit_switch_state() == False and \
            self.driver.get_upper_limit_switch_state() == False:
            return DOOR_POSITION_INTERMEDIATE
        elif self.driver.get_lower_limit_switch_state() == True and \
            self.driver.get_upper_limit_switch_state() == False:
            return DOOR_POSITION_CLOSED
        elif self.driver.get_lower_limit_switch_state() == False and \
            self.driver.get_upper_limit_switch_state() == True:
            return DOOR_POSITION_OPEN
        else:
            return DOOR_POSITION_ERROR

    def _switch_changed(self, sender):
        """Callback method, which is called by the driver by emitting a certain
        signal."""
        logger.debug("Limit switches have changed their state to %d", self.get_door_position())

        if self._check_for_error_condition() == False:
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
        logger.debug("Trigger timeout occured")
        self.trigger_timer = False
        self.stop_door_signal()

    def set_intent(self, new_intent_name):
        """Instantiate a new intent object by its name."""
        logger.debug("Setting new intent: " + new_intent_name)
        intent_module = importlib.import_module("garage.door.intents." + new_intent_name.lower() + "_intent")
        self.intent = getattr(intent_module, new_intent_name + "Intent")(self)

        self.intent.start()
