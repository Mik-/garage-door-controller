import importlib
from threading import Timer
from positions import *
from blinker import signal
from signals import *

class Door(object):
    def __init__(self, name, driver, transit_time, trigger_time):
        self.name = name
        self.driver = driver
        self.trigger_timer = False
        self.state = False # Init variable to prevent error on first call of set_new_state
        if self._check_for_error_condition() == True:
            self.set_new_state("Error")
        else:
            self.set_new_state("Init")
        self.tansit_time = transit_time     # time, the door need for opening or closing
        self.trigger_time = trigger_time    # time, the relais will triggered to move door
        signal(SIGNAL_LOWER_SWITCH_CHANGED).connect(self._switch_changed)
        signal(SIGNAL_UPPER_SWITCH_CHANGED).connect(self._switch_changed)

    def __del__(self):
        signal(SIGNAL_LOWER_SWITCH_CHANGED).disconnect(self._switch_changed)
        signal(SIGNAL_UPPER_SWITCH_CHANGED).disconnect(self._switch_changed)

    def start_door_signal(self):
        """Triggers the physical door controller by closing the relais for
        the defined amount of time"""
        self.driver.start_door_signal()

        if self.trigger_timer:
            self.trigger_timer.cancel()
        self.trigger_timer = Timer(self.trigger_time, self._trigger_timeout)
        self.trigger_timer.start()

    def stop_door_signal(self):
        self.driver.stop_door_signal()
        if self.trigger_timer:
            self.trigger_timer.cancel()
            self.trigger_timer = False

    def set_new_state(self, new_state_name):
        if self.state:
            self.state.exit()
        state_module = importlib.import_module("garage.door.states." + new_state_name.lower() + "_state")
        self.state = getattr(state_module, new_state_name + "State")(self)
        self.state.enter()

    def get_door_position(self):
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
        if self._check_for_error_condition() == False:
            self.state.door_position_changed(self.get_door_position())

    def _check_for_error_condition(self):
        if self.get_door_position() == DOOR_POSITION_ERROR:
            self.set_new_state("Error")
            return True
        else:
            return False

    def _trigger_timeout(self):
        self.trigger_timer = False
        self.stop_door_signal()
