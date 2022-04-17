import os

import Utility.dialog_windows as window

# kivy
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget

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
        self.start_battle_popup = Popup()
        self.buy_tank_popup = Popup()
        self.battle_popup = Popup()

    def open_dialog(self, mode: str):
        if mode == "account":
            self.dialog = window.AccountWindow(model=self.model)
        elif mode == "rename":
            self.dialog = window.RenameWindow(model=self.model)

        self.dialog.open()
        self.controller.dialog(mode, self.dialog)

    def close_dialog(self, dialog_data: list = []):
        if self.dialog.mode == "account":
            self.controller.change_account(dialog_data)
        elif self.dialog.mode == "rename":
            self.controller.change_nickname(dialog_data)
        self.dialog = None


    # Button pressed actions
    def play_is(self, obj):
        self.controller.start_battle(1)

    def buy_is(self, obj):
        self.controller.buy_tank(1)

    def play_t34(self, obj):
        self.controller.start_battle(2)

    def buy_t34(self, obj):
        self.controller.buy_tank(2)

    def play_su(self, obj):
        self.controller.start_battle(3)

    def buy_su(self, obj):
        self.controller.buy_tank(3)

    def model_is_changed(self, data):
        """ The method is called when the model changes. """
        self.close_dialog(data)



    # start battle popups
    def open_start_battle_popup(self, obj):
        layout = GridLayout(cols=3, spacing=[10])

        # add imgs
        img1 = Image(source='img/is.jpg')
        layout.add_widget(img1)
        img2 = Image(source='img/isu.jpg')
        layout.add_widget(img2)
        img3 = Image(source='img/t34.jpg')
        layout.add_widget(img3)

        # add buttons
        button1 = Button(text='Start',
                         on_press=self.play_is)
        layout.add_widget(button1)
        button2 = Button(text='Start',
                         on_press=self.play_su)
        layout.add_widget(button2)
        button3 = Button(text='Start',
                         on_press=self.play_t34)
        layout.add_widget(button3)

        # add last row with close button
        widget1 = Widget()
        widget2 = Widget()
        closeButton = Button(text='Close',
                             on_press=self.close_start_battle_popup)
        layout.add_widget(widget1)
        layout.add_widget(closeButton)
        layout.add_widget(widget2)

        self.start_battle_popup = Popup(title="Start battle",
                                        content=layout,
                                        size_hint=(None, None),
                                        size=(400, 250),
                                        auto_dismiss=False)
        self.start_battle_popup.open()

    def close_start_battle_popup(self, obj):
        self.start_battle_popup.dismiss()



    # buy tanks popups
    def open_buy_tank_popup(self, obj):
        layout = GridLayout(cols=3, spacing=[10])
        prices = self.controller.get_prices()

        # add imgs
        img1 = Image(source='img/is.jpg')
        layout.add_widget(img1)
        img2 = Image(source='img/isu.jpg')
        layout.add_widget(img2)
        img3 = Image(source='img/t34.jpg')
        layout.add_widget(img3)

        # add prices
        for price in prices:
            label = Label(text=price)
            layout.add_widget(label)

        # add buttons
        button1 = Button(text='Buy',
                         on_press=self.buy_is)
        layout.add_widget(button1)
        button2 = Button(text='Buy',
                         on_press=self.buy_su)
        layout.add_widget(button2)
        button3 = Button(text='Buy',
                         on_press=self.buy_t34)
        layout.add_widget(button3)

        # add last row with close button
        widget1 = Widget()
        widget2 = Widget()
        closeButton = Button(text='Close',
                             on_press=self.close_buy_tank_popup)
        layout.add_widget(widget1)
        layout.add_widget(closeButton)
        layout.add_widget(widget2)

        self.buy_tank_popup = Popup(title="Buy tank",
                                    content=layout,
                                    size_hint=(None, None),
                                    size=(400, 250),
                                    auto_dismiss=False)
        self.buy_tank_popup.open()

    def close_buy_tank_popup(self, obj):
        self.buy_tank_popup.dismiss()



    # battle popups!!!!!!!!!!!!!!!!!!!!!!!!!!
    def open_battle_popup(self, obj):
        pass

    def close_battle_popup(self, obj):
        self.battle_popup.dismiss()



    def refresh(self):
        self.controller.refresh()

    def build(self):
        self.add_widget(self.model.table)
        return self


# load interface from kv file
Builder.load_file(os.path.join(os.path.dirname(__file__), "myscreen.kv"))
