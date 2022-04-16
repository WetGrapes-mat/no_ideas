import os

import Utility.dialog_windows as window

# kivy
from kivy.properties import ObjectProperty
from kivy.lang import Builder

# kivyMD
from kivymd.uix.screen import MDScreen
from kivymd.uix.screen import Screen
from kivymd.uix.snackbar import Snackbar


from Utility.observer import Observer


class MyScreenView(MDScreen, Observer):
    """ A class that implements the visual presentation `MyScreenModel`. """

    # <Controller.myscreen_controller.MyScreenController object>.
    controller = ObjectProperty()
    # <Model.myscreen.MyScreenModel object>.
    model = ObjectProperty()


    def __init__(self, **kw):
        super().__init__(**kw)
        self.model.add_observer(self)  # register the view as an observer
        self.screen = Screen() 


    def open_dialog(self, mode: str):
        if mode == "account":
            self.dialog = window.AccountWindow(model=self.model)
        elif mode == "rename":
            self.dialog = window.RenameWindow(model=self.model)

        self.dialog.open()
        self.controller.dialog(mode, self.dialog)
        

    def close_dialog(self, dialog_data: list=[]):
        if self.dialog.mode == "account":
            self.controller.change_account(dialog_data)
        elif self.dialog.mode == "rename":
            self.controller.change_nickname(dialog_data)
        self.dialog = None

    def play_is(self, obj):
        self.controller.start_battle(1)

    def play_t34(self, obj):
        self.controller.start_battle(2)

    def play_su(self, obj):
        self.controller.start_battle(3)

    def model_is_changed(self, data):
        """ The method is called when the model changes. """
        self.close_dialog(data)
    

    def refresh(self):
        self.controller.refresh() 


    def build(self):
        self.add_widget(self.model.table)
        return self



#load interface from kv file
Builder.load_file(os.path.join(os.path.dirname(__file__), "myscreen.kv"))