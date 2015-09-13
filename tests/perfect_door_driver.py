from garage.door.driver import Driver
from threading import Timer
from blinker import signal
from garage.door.signals import *
import logging

logger = logging.getLogger("tests." + __name__)

class PerfectDoorDriver(Driver):
    """This driver emulates a perfect door."""
    def __init__(self, transit_time, accelerate_time):
        self.transit_time = transit_time
        self.transit_timer = False
        self.accelerate_time = accelerate_time
        self.accelerate_timer = False
        self.door_signal = False
        self.door_signal_toggled = False
        self.upper_limit_switch = False
        self.lower_limit_switch = True

    def cleanup(self):
        # nothing to cleanup here
        logger.debug("Cleanup.")
        if self.transit_timer:
            self.transit_timer.cancel()
        if self.accelerate_timer:
            self.accelerate_timer.cancel()

    def start_door_signal(self):
        logger.debug("door signal started")
        if self.door_signal == False:
            self.door_signal_toggled = True
        self.door_signal = True

        if self.lower_limit_switch:
            self.last_direction_up = True
        else:
            self.last_direction_up = False

        if self.accelerate_timer:
            self.accelerate_timer.cancel()
        self.accelerate_timer = Timer(self.accelerate_time, self._accelerate_timer_timeout)
        self.accelerate_timer.start()

        if self.transit_timer:
            self.transit_timer.cancel()
        self.transit_timer = Timer(self.transit_time, self._transit_timer_timeout)
        self.transit_timer.start()

    def stop_door_signal(self):
        logger.debug("door signal stopped")
        if self.door_signal == True:
            self.door_signal_toggled = True
        self.door_signal = False

    def get_upper_limit_switch_state(self):
        return self.upper_limit_switch

    def get_lower_limit_switch_state(self):
        return self.lower_limit_switch

    def _accelerate_timer_timeout(self):
        self.accelerate_timer = False

        if self.lower_limit_switch:
            self.lower_limit_switch = False
            signal(SIGNAL_LOWER_SWITCH_CHANGED).send(self)
        elif self.upper_limit_switch:
            self.upper_limit_switch = False
            signal(SIGNAL_UPPER_SWITCH_CHANGED).send(self)

    def _transit_timer_timeout(self):
        self.transit_timer = False

        if self.last_direction_up:
            self.upper_limit_switch = True
            signal(SIGNAL_UPPER_SWITCH_CHANGED).send(self)
        else:
            self.lower_limit_switch = True
            signal(SIGNAL_LOWER_SWITCH_CHANGED).send(self)
