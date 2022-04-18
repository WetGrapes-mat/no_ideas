# The model implements the observer pattern. This means that the class must
# support adding, removing, and alerting observers. In this case, the model is
# completely independent of controllers and views. It is important that all
# registered observers implement a specific method that will be called by the
# model when they are notified (in this case, it is the `model_is_changed`
# method). For this, observers must be descendants of an abstract class,
# inheriting which, the `model_is_changed` method must be overridden.

import re

# parsers
from Utility.parsers.dom_writer import DomWriter
from Utility.parsers.sax_reader import SaxReader


class MyScreenModel:
    """
    The MyScreenModel class is a data model implementation. The model stores
    the values of the variables `c`, `d` and their sum. The model provides an
    interface through which to work with stored values. The model contains
    methods for registration, deletion and notification observers.

    The model is (primarily) responsible for the logic of the application.
    MyScreenModel class task is to add two numbers.
    """

    # list of row data that are hidden
    _not_filtered = []


    def __init__(self):
        self.dialog = None
        self._observers = []
        self.s = Server()
        self.player = s.get_player_list()[0]

    # observers
    def add_observer(self, observer):
        self._observers.append(observer)


    def remove_observer(self, observer):
        self._observers.remove(observer)


    def notify_observers(self, data):
        for x in self._observers:
            x.model_is_changed(data)


    def choose_account(self, nick: str):
        for i in range(len(self.s.get_player_list())):
            if self.s.get_player_list()[i].get_nickname() == nick:
                self.player = self.s.get_player_list()[i]
                return True
        return False

    def change_nickname(self, newnick: str):
        return self.player.change_nickname(self.s, newnick)

    def buy_tank(self, tank):
        return self.player.buy_tank(self.s, tank)

    def start_battle(self, tank):
        return self.player.lets_battle(self.s)


    def get_account_info(self):
        name = ""
        credits = ""
        tanks = []
        return name, credits, tanks
    #get player info: name, credits, tanks [1,2,3] - has all




    def open_dialog(self, dialog, mode):
        self.dialog = dialog 

    def close_dialog(self, dialog_data: list=[]):
        data = dialog_data
        self.notify_observers(data)
        self.dialog = None