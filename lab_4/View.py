import os

import dialog_windows as window

# kivy
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget

# kivyMD
from kivymd.uix.screen import MDScreen
from kivymd.uix.screen import Screen
from kivymd.uix.snackbar import Snackbar

from observer import Observer


class MyScreenView(MDScreen, Observer):
    """ A class that implements the visual presentation `MyScreenModel`. """

    # cont = ObjectProperty()
    # mod = ObjectProperty()
    information = {'is': None,
                   'isu': None,
                   't34': None}


    def __init__(self, c, m, **kw):
        super().__init__(**kw)

        self.model = m
        self.model.add_observer(self)
        self.controller = c
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
            posibility = self.controller.change_account(dialog_data)
            if posibility:
                Snackbar(text="Account was changed").open()
            else:
                Snackbar(text="Account wasn't changed").open()
        elif self.dialog.mode == "rename":
            posibility = self.controller.change_nickname(dialog_data)
            if posibility:
                Snackbar(text="Name was changed").open()
            else:
                Snackbar(text="Name wasn't changed").open()
        self.update()
        self.dialog = None

    # Button pressed actions


    def play_is(self, obj):
        self.controller.start_battle('IS')

    def buy_is(self, obj):
        self.controller.buy_tank('IS')

    def play_t34(self, obj):
        self.controller.start_battle('T-34')

    def buy_t34(self, obj):
        self.controller.buy_tank('T-34')

    def play_su(self, obj):
        self.controller.start_battle('SU-100')

    def buy_su(self, obj):
        self.controller.buy_tank('SU-100')

    def model_is_changed(self, data):
        """ The method is called when the model changes. """
        self.close_dialog(data)

    # start battle popups
    def open_start_battle_popup(self):
        layout = GridLayout(cols=3, spacing=[10])

        # add imgs

        img1 = Image(source='img/is.jpg')
        layout.add_widget(img1)
        img2 = Image(source='img/isu.jpg')
        layout.add_widget(img2)
        img3 = Image(source='img/t34.jpg')
        layout.add_widget(img3)

        # add buttons
        button1 = Button(text="You don't have this tank",
                         on_press=self.close_start_battle_popup,
                         on_release=self.play_is,
                         disabled=True)
        layout.add_widget(button1)
        button2 = Button(text="You don't have this tank",
                         on_press=self.close_start_battle_popup,
                         on_release=self.play_su,
                         disabled=True)
        layout.add_widget(button2)
        button3 = Button(text="You don't have this tank",
                         on_press=self.close_start_battle_popup,
                         on_release=self.play_t34,
                         disabled=True)
        layout.add_widget(button3)

        for i in self.model.player.get_tanks():
            if i.get_id() == 1:
                button3.disabled = False
                button3.text = 'Start'
            elif i.get_id() == 2:
                button1.disabled = False
                button1.text = 'Start'
            elif i.get_id() == 3:
                button2.disabled = False
                button2.text = 'Start'

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
                                        size=(1000, 850),
                                        auto_dismiss=False)
        self.start_battle_popup.open()

    def close_start_battle_popup(self, obj):
        self.start_battle_popup.dismiss()

    # buy tanks popups
    def open_buy_tank_popup(self):
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
                         on_press=self.buy_is,
                         #on_release=self.close_buy_tank_popup,
                         disabled=False)
        layout.add_widget(button1)
        button2 = Button(text='Buy',
                         on_press=self.buy_su,
                         #on_release=self.close_buy_tank_popup,
                         disabled=False)
        layout.add_widget(button2)
        button3 = Button(text='Buy',
                         on_press=self.buy_t34,
                         #on_release=self.close_buy_tank_popup,
                         disabled=False)
        layout.add_widget(button3)

        for i in self.model.player.get_tanks():
            if i.get_id() == 1:
                button3.disabled = True
                button3.text = 'You already have this tank'
            elif i.get_id() == 2:
                button1.disabled = True
                button1.text = 'You already have this tank'
            elif i.get_id() == 3:
                button2.disabled = True
                button2.text = 'You already have this tank'


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
                                    size=(1000, 850),
                                    auto_dismiss=False)
        self.buy_tank_popup.open()

    def close_buy_tank_popup(self, obj):
        self.update()
        self.buy_tank_popup.dismiss()


    def open_battle_popup(self, credits, text, info):
        layout = BoxLayout(orientation="vertical")

        for itteration in info.key:
            for event in itteration:
                if len(event) == 3:
                    event_label = Label(text="{:^15} damaged {:^5} {:^15} ".format(event[0].rstrip(),
                                                                                   event[1].rstrip(),
                                                                                   event[2].rstrip()))
                    layout.add_widget(event_label)
                if len(event) == 2:
                    event_label = Label(text="{:^15}  {:^11}  {:^15}".format(event[0].rstrip(),
                                                                             'Killed',
                                                                             event[1].rstrip()))
                    layout.add_widget(event_label)

        text_label = Label(text="Boobs", size_hint=(1, 0.8))
        layout.add_widget(text_label)

        credits_label = Label(text="You earned {} credits for this battle".format(credits),
                              size_hint=(1, 0.1))
        layout.add_widget(credits_label)

        close_button = Button(text='Close',
                              size_hint=(1, 0.1),
                              on_press=self.close_battle_popup)
        layout.add_widget(close_button)


        self.battle_popup = Popup(title="Battle finished",
                                        content=layout,
                                        size_hint=(None, None),
                                        size=(600, 1000),
                                        auto_dismiss=False)
        self.battle_popup.open()

    def close_battle_popup(self, obj):
        self.battle_popup.dismiss()

    def refresh(self):
        self.controller.refresh()

    def update(self):
        nickname, credts, tanks = self.controller.get_account_info()
        self.information['nik'].text = nickname
        self.information['credits'].text = credts
        self.information['t34'].source = 'img/off.svg.png'
        self.information['is'].source = 'img/off.svg.png'
        self.information['isu'].source = 'img/off.svg.png'
        for i in tanks:
            if i == 1:
                self.information['t34'].source = 'img/t34.jpg'
            elif i == 2:
                self.information['is'].source = 'img/is.jpg'
            if i == 3:
                self.information['isu'].source = 'img/isu.jpg'

    def build(self):
        nickname, credts, tanks = self.controller.get_account_info()

        layout = GridLayout(cols=3, spacing=[10])

        widget1 = Widget()
        nick_label = Label(text=nickname)
        credits_label = Label(text='Кредиты: ' + credts)
        self.information['nik'] = nick_label
        self.information['credits'] = credits_label

        layout.add_widget(widget1)
        layout.add_widget(nick_label)
        layout.add_widget(credits_label)

        img1 = Image(source='img/off.svg.png')
        self.information['t34'] = img1
        layout.add_widget(img1)
        # if tanks.count(2) > 0:
        img2 = Image(source='img/off.svg.png')
        self.information['is'] = img2
        layout.add_widget(img2)
        # if tanks.count(3) > 0:
        img3 = Image(source='img/off.svg.png')
        self.information['isu'] = img3
        layout.add_widget(img3)

        self.add_widget(layout)
        # Builder.load_file(os.path.join(os.path.dirname(__file__), "myscreen.kv"))
        print(self.information)
        self.update()
        return self


# load interface from kv file
Builder.load_file(os.path.join(os.path.dirname(__file__), "myscreen.kv"))
