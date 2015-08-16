class Driver:
    """This is a absract hardware driver class.

    All drivers have to implement the folowing methods."""

    def start_door_signal(self):
        """Start signal to vendor controller to move the door. In most cases
        a relais is switched on."""
        raise NotImplementedError("Class %s doesn't implement start_door_signal()"
            % (self.__class__.__name__))

    def stop_door_signal(self):
        """Stop signal to vendor controller to move the door. In most cases
        a relais is switched off."""
        raise NotImplementedError("Class %s doesn't implement stop_door_signal()"
            % (self.__class__.__name__))

    def get_upper_limit_switch_state(self):
        """Returns the state of the upper limit switch. If the door is located
        in the upper position, this method should return True."""
        raise NotImplementedError("Class %s doesn't implement get_upper_limit_switch_state()"
            % (self.__class__.__name__))

    def get_lower_limit_switch_state(self):
        """Returns the state of the lower limit switch. If the door is located
        in the lower position, this method should return True."""
        raise NotImplementedError("Class %s doesn't implement get_lower_limit_switch_state()"
            % (self.__class__.__name__))
