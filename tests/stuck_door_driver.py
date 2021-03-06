"""
Simulates a door, which stucks on first trigger.
"""

import logging
from blinker import signal
from perfect_door_driver import PerfectDoorDriver
from garage.door.signals import SIGNAL_LOWER_SWITCH_CHANGED, SIGNAL_UPPER_SWITCH_CHANGED

LOGGER = logging.getLogger("tests." + __name__)

class StuckDoorDriver(PerfectDoorDriver):
    """This driver emulates a door wich stucks on first trigger."""
    def __init__(self, transit_time, accelerate_time):
        super(StuckDoorDriver, self).__init__(transit_time, accelerate_time)
        self.stuck_count = 0
        self.instance = self

    def start_door_signal(self):
        self.stuck_count += 1
        super(StuckDoorDriver, self).start_door_signal()

    def _accelerate_timer_timeout(self):
        self.accelerate_timer = False

        if self.stuck_count >= 2:
            if self.lower_limit_switch:
                self.lower_limit_switch = False
                signal(SIGNAL_LOWER_SWITCH_CHANGED).send(self.instance)
            elif self.upper_limit_switch:
                self.upper_limit_switch = False
                signal(SIGNAL_UPPER_SWITCH_CHANGED).send(self.instance)
        elif self.transit_timer:
            self.transit_timer.cancel()
            self.transit_timer = False

    def _transit_timer_timeout(self):
        self.stuck_count = 0
        super(StuckDoorDriver, self)._transit_timer_timeout()
