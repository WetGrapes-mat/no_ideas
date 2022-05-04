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

    # players imgs
    img_1 = Image()
    img_2 = Image()
    img_3 = Image()
    img_4 = Image()
    img_5 = Image()
    img_6 = Image()
    img_7 = Image()
    img_8 = Image()
    img_9 = Image()
    img_10 = Image()
    img_11 = Image()
    img_12 = Image()
    img_13 = Image()
    img_14 = Image()


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

    # battle popups!!!!!!!!!!!!!!!!!!!!!!!!!!

    def open_battle_popup(self, battle, mapname):
        # battle = [ ("nick",<num_tank>),("nick", <num_tank>)  ]
        # num_tank: 1-IS, 2 - T34, 3 - SU
        # odd - 1st team
        # even - 2nd team
        layout = GridLayout(cols=3, spacing=[10])

        # map name row
        widget1 = Widget()
        widget2 = Widget()
        mapname_label = Label(text=mapname, size_hint=(1, .1))
        layout.add_widget(widget1)
        layout.add_widget(mapname_label)
        layout.add_widget(widget2)

        # players

        nick, tank = battle[0]
        player_layout = BoxLayout(orientation='vertical')
        if tank == 1:
            self.img_1 = Image(source='img/is.jpg', size_hint=(1, 1))
            player_layout.add_widget(self.img_1)
        if tank == 2:
            self.img_1 = Image(source='img/t34.jpg', size_hint=(1, 1))
            player_layout.add_widget(self.img_1)
        if tank == 3:
            self.img_1 = Image(source='img/isu.jpg', size_hint=(1, 1))
            player_layout.add_widget(self.img_1)
        nick_label = Label(text=nick, size_hint=(1, .1))
        player_layout.add_widget(nick_label)

        layout.add_widget(player_layout)
        widget1 = Widget()
        layout.add_widget(widget1)

        nick, tank = battle[1]
        player_layout = BoxLayout(orientation='vertical')
        if tank == 1:
            self.img_2 = Image(source='img/is.jpg', size_hint=(1, 1))
            player_layout.add_widget(self.img_2)
        if tank == 2:
            self.img_2 = Image(source='img/t34.jpg', size_hint=(1, 1))
            player_layout.add_widget(self.img_2)
        if tank == 3:
            self.img_2 = Image(source='img/isu.jpg', size_hint=(1, 1))
            player_layout.add_widget(self.img_2)
        nick_label = Label(text=nick, size_hint=(1, .1))
        player_layout.add_widget(nick_label)
        layout.add_widget(player_layout)

        nick, tank = battle[2]
        player_layout = BoxLayout(orientation='vertical')
        if tank == 1:
            self.img_3 = Image(source='img/is.jpg', size_hint=(1, 1))
            player_layout.add_widget(self.img_3)
        if tank == 2:
            self.img_3 = Image(source='img/t34.jpg', size_hint=(1, 1))
            player_layout.add_widget(self.img_3)
        if tank == 3:
            self.img_3 = Image(source='img/isu.jpg', size_hint=(1, 1))
            player_layout.add_widget(self.img_3)
        nick_label = Label(text=nick, size_hint=(1, .1))
        player_layout.add_widget(nick_label)

        layout.add_widget(player_layout)
        widget1 = Widget()
        layout.add_widget(widget1)

        nick, tank = battle[3]
        player_layout = BoxLayout(orientation='vertical')
        if tank == 1:
            self.img_4 = Image(source='img/is.jpg', size_hint=(1, 1))
            player_layout.add_widget(self.img_4)
        if tank == 2:
            self.img_4 = Image(source='img/t34.jpg', size_hint=(1, 1))
            player_layout.add_widget(self.img_4)
        if tank == 3:
            self.img_4 = Image(source='img/isu.jpg', size_hint=(1, 1))
            player_layout.add_widget(self.img_4)
        nick_label = Label(text=nick, size_hint=(1, .1))
        player_layout.add_widget(nick_label)
        layout.add_widget(player_layout)

        nick, tank = battle[4]
        player_layout = BoxLayout(orientation='vertical')
        if tank == 1:
            self.img_5 = Image(source='img/is.jpg', size_hint=(1, 1))
            player_layout.add_widget(self.img_5)
        if tank == 2:
            self.img_5 = Image(source='img/t34.jpg', size_hint=(1, 1))
            player_layout.add_widget(self.img_5)
        if tank == 3:
            self.img_5 = Image(source='img/isu.jpg', size_hint=(1, 1))
            player_layout.add_widget(self.img_5)
        nick_label = Label(text=nick, size_hint=(1, .1))
        player_layout.add_widget(nick_label)

        layout.add_widget(player_layout)
        widget1 = Widget()
        layout.add_widget(widget1)

        nick, tank = battle[5]
        player_layout = BoxLayout(orientation='vertical')
        if tank == 1:
            self.img_6 = Image(source='img/is.jpg', size_hint=(1, 1))
            player_layout.add_widget(self.img_6)
        if tank == 2:
            self.img_6 = Image(source='img/t34.jpg', size_hint=(1, 1))
            player_layout.add_widget(self.img_6)
        if tank == 3:
            self.img_6 = Image(source='img/isu.jpg', size_hint=(1, 1))
            player_layout.add_widget(self.img_6)
        nick_label = Label(text=nick, size_hint=(1, .1))
        player_layout.add_widget(nick_label)
        layout.add_widget(player_layout)

        nick, tank = battle[6]
        player_layout = BoxLayout(orientation='vertical')
        if tank == 1:
            self.img_7 = Image(source='img/is.jpg', size_hint=(1, 1))
            player_layout.add_widget(self.img_7)
        if tank == 2:
            self.img_7 = Image(source='img/t34.jpg', size_hint=(1, 1))
            player_layout.add_widget(self.img_7)
        if tank == 3:
            self.img_7 = Image(source='img/isu.jpg', size_hint=(1, 1))
            player_layout.add_widget(self.img_7)
        nick_label = Label(text=nick, size_hint=(1, .1))
        player_layout.add_widget(nick_label)

        layout.add_widget(player_layout)
        widget1 = Widget()
        layout.add_widget(widget1)

        nick, tank = battle[7]
        player_layout = BoxLayout(orientation='vertical')
        if tank == 1:
            self.img_8 = Image(source='img/is.jpg', size_hint=(1, 1))
            player_layout.add_widget(self.img_8)
        if tank == 2:
            self.img_8= Image(source='img/t34.jpg', size_hint=(1, 1))
            player_layout.add_widget(self.img_8)
        if tank == 3:
            self.img_8= Image(source='img/isu.jpg', size_hint=(1, 1))
            player_layout.add_widget(self.img_8)
        nick_label = Label(text=nick, size_hint=(1, .1))
        player_layout.add_widget(nick_label)
        layout.add_widget(player_layout)

        nick, tank = battle[8]
        player_layout = BoxLayout(orientation='vertical')
        if tank == 1:
            self.img_9 = Image(source='img/is.jpg', size_hint=(1, 1))
            player_layout.add_widget(self.img_9)
        if tank == 2:
            self.img_9 = Image(source='img/t34.jpg', size_hint=(1, 1))
            player_layout.add_widget(self.img_9)
        if tank == 3:
            self.img_9 = Image(source='img/isu.jpg', size_hint=(1, 1))
            player_layout.add_widget(self.img_9)
        nick_label = Label(text=nick, size_hint=(1, .1))
        player_layout.add_widget(nick_label)

        layout.add_widget(player_layout)
        widget1 = Widget()
        layout.add_widget(widget1)

        nick, tank = battle[9]
        player_layout = BoxLayout(orientation='vertical')
        if tank == 1:
            self.img_10 = Image(source='img/is.jpg', size_hint=(1, 1))
            player_layout.add_widget(self.img_10)
        if tank == 2:
            self.img_10 = Image(source='img/t34.jpg', size_hint=(1, 1))
            player_layout.add_widget(self.img_10)
        if tank == 3:
            self.img_10 = Image(source='img/isu.jpg', size_hint=(1, 1))
            player_layout.add_widget(self.img_10)
        nick_label = Label(text=nick, size_hint=(1, .1))
        player_layout.add_widget(nick_label)
        layout.add_widget(player_layout)

        nick, tank = battle[10]
        player_layout = BoxLayout(orientation='vertical')
        if tank == 1:
            self.img_11 = Image(source='img/is.jpg', size_hint=(1, 1))
            player_layout.add_widget(self.img_11)
        if tank == 2:
            self.img_11 = Image(source='img/t34.jpg', size_hint=(1, 1))
            player_layout.add_widget(self.img_11)
        if tank == 3:
            self.img_11 = Image(source='img/isu.jpg', size_hint=(1, 1))
            player_layout.add_widget(self.img_11)
        nick_label = Label(text=nick, size_hint=(1, .1))
        player_layout.add_widget(nick_label)

        layout.add_widget(player_layout)
        widget1 = Widget()
        layout.add_widget(widget1)

        nick, tank = battle[11]
        player_layout = BoxLayout(orientation='vertical')
        if tank == 1:
            self.img_12 = Image(source='img/is.jpg', size_hint=(1, 1))
            player_layout.add_widget(self.img_12)
        if tank == 2:
            self.img_12 = Image(source='img/t34.jpg', size_hint=(1, 1))
            player_layout.add_widget(self.img_12)
        if tank == 3:
            self.img_12 = Image(source='img/isu.jpg', size_hint=(1, 1))
            player_layout.add_widget(self.img_12)
        nick_label = Label(text=nick, size_hint=(1, .1))
        player_layout.add_widget(nick_label)
        layout.add_widget(player_layout)

        nick, tank = battle[12]
        player_layout = BoxLayout(orientation='vertical')
        if tank == 1:
            self.img_13 = Image(source='img/is.jpg', size_hint=(1, 1))
            player_layout.add_widget(self.img_13)
        if tank == 2:
            self.img_13 = Image(source='img/t34.jpg', size_hint=(1, 1))
            player_layout.add_widget(self.img_13)
        if tank == 3:
            self.img_13 = Image(source='img/isu.jpg', size_hint=(1, 1))
            player_layout.add_widget(self.img_13)
        nick_label = Label(text=nick, size_hint=(1, .1))
        player_layout.add_widget(nick_label)

        layout.add_widget(player_layout)
        widget1 = Widget()
        layout.add_widget(widget1)

        nick, tank = battle[13]
        player_layout = BoxLayout(orientation='vertical')
        if tank == 1:
            self.img_14 = Image(source='img/is.jpg', size_hint=(1, 1))
            player_layout.add_widget(self.img_14)
        if tank == 2:
            self.img_14 = Image(source='img/t34.jpg', size_hint=(1, 1))
            player_layout.add_widget(self.img_14)
        if tank == 3:
            self.img_14 = Image(source='img/isu.jpg', size_hint=(1, 1))
            player_layout.add_widget(self.img_14)
        nick_label = Label(text=nick, size_hint=(1, .1))
        player_layout.add_widget(nick_label)
        layout.add_widget(player_layout)

        self.battle_popup = Popup(title="Battle",
                                        content=layout,
                                        size_hint=(None, None),
                                        size=(400, 1000),
                                        auto_dismiss=False)
        self.battle_popup.open()

    def close_battle_popup(self, obj):
        self.battle_popup.dismiss()

    def print_earned_money(self, earned_money):
        Snackbar(text="You've just earned {} credits".format(earned_money)).open()

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
