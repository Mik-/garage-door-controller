"""
This is a mock for the driver interface.
"""
import logging
from garage.door.driver import Driver

LOGGER = logging.getLogger("tests." + __name__)

class MockDriver(Driver):
    """
    Mocking class for driver interface.
    """
    def __init__(self):
        self.door_signal = False
        self.door_signal_toggled = False
        self.upper_limit_switch = False
        self.lower_limit_switch = False
        self.trigger_count = False

    def cleanup(self):
        # nothing to cleanup here
        LOGGER.debug("MockDriver cleanup.")

    def start_door_signal(self):
        LOGGER.debug("door signal started")
        if not self.door_signal:
            self.door_signal_toggled = True
        self.door_signal = True

    def stop_door_signal(self):
        LOGGER.debug("door signal stopped")
        if self.door_signal:
            self.door_signal_toggled = True
            self.trigger_count += 1
        self.door_signal = False

    def get_upper_limit_switch_state(self):
        return self.upper_limit_switch

    def get_lower_limit_switch_state(self):
        return self.lower_limit_switch
