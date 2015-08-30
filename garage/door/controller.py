from model import door
from tools.observerpattern.observer import Observer

class Controller(Observer):
    def __init__(self, model):
        self.model = model
        self.model.register(self)

    def update(self, *args, **kwargs):
        """Method will be called as callback of the subject class"""
        pass

    def open_door(self):
        """Opens the door"""
        if self.model
