"""This module provieds the interface for the state classes and the StateFactory."""

import importlib
from abc import ABCMeta, abstractmethod

class State(object):
    """This abstract class builds the interface for all state classes."""
    __metaclass__ = ABCMeta

    def __init__(self):
        self.actions = dict()

    @abstractmethod
    def door_position_changed(self, new_position):
        """This method is called by the door model, when its positions is changed."""
        raise NotImplementedError

    @abstractmethod
    def enter(self):
        """This method is called by the door model, if this state is entered."""
        raise NotImplementedError

    @abstractmethod
    def exit(self):
        """This method is called by the door model, if this state is exited."""
        raise NotImplementedError

    def register_action(self, intent_name, action):
        """This method adds an action for the given intent.

        Args:
            intent_name (str): The name of the intent, for which the action is registered.
            action: A method, which is called, to reach the intent.
        """

        if intent_name in self.actions:
            raise Exception("Action for intent %s already exists!", intent_name)
        else:
            self.actions[intent_name] = action

    def get_action(self, intent_name):
        """This method returns an action, which is necessary to reach the desired intent.

        Args:
            intent_name (str): The desired intent.

        Returns:
            A method, which is called by the door model. This method has to do all
            actions, which are necessary to reach teh desired intent. Then method
            takes the door model as parameter.
        """

        if intent_name in self.actions:
            return self.actions[intent_name]
        else:
            return None


class StateFactory(object):
    """This class creates a state by name by calling the desired state factory."""

    @staticmethod
    def create_state(state_name, door_model):
        """Returns a new instance of the state class, described by state_name.

        Args:
            state_name (str): The name of the state class without 'State'.
            door_model: The door model to assign to the new state class.

        Returns:
            A new instance of the state class, described by state_name.
        """

        # Find the module with the desired state
        state_module = importlib.import_module("garage.door.states." +
                                               state_name.lower() + "_state")

        # Get the state factory
        state_factory_class = getattr(state_module, state_name + "StateFactory")

        # Return an instance of desired state
        return state_factory_class.create_state(door_model)

