from garage.door.driver import Driver

class MockDriver(Driver):
    def __init__(self):
        self.door_signal = False
        self.door_signal_toggled = False
        self.upper_limit_switch = False
        self.lower_limit_switch = False

    def start_door_signal(self):
        if self.door_signal == False:
            self.door_signal_toggled = True
        self.door_signal = True

    def stop_door_signal(self):
        if self.door_signal == True:
            self.door_signal_toggled = True
        self.door_signal = False

    def get_upper_limit_switch_state(self):
        return self.upper_limit_switch

    def get_lower_limit_switch_state(self):
        return self.lower_limit_switch
