"""This module provieds the interface for the state classes."""

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

    def add_action(self, intent_name, action):
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
