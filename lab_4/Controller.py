# from View.myscreen import MyScreenView

from View import MyScreenView


class MyScreenController:
    """
    The `MyScreenController` class represents a controller implementation.
    Coordinates work of the view with the model.

    The controller implements the strategy pattern. The controller connects to
    the view to control its actions.
    """

    def __init__(self, model):
        """
        The constructor takes a reference to the model.
        The constructor creates the view.
        """
        self.model = model
        self.view = MyScreenView(self, self.model)

    def refresh(self):
        self.model.refresh_students_in_table()

    def get_screen(self):
        """The method creates get the view."""
        return self.view.build()

    # ready
    def change_account(self, data):
        return self.model.choose_account(nick=data)

    def change_nickname(self, data):
        return self.model.change_nickname(newnick=data)

    def start_battle(self, tank):
        self.view.close_start_battle_popup("")
        credits, text, view_info = self.model.start_battle(tank)
        self.battle_popup(view_info['iter'], view_info['info'])
        self.view.update()

    def buy_tank(self, tank):
        return self.model.buy_tank(tank)

    def get_account_info(self):
        return self.model.get_account_info()

    def battle_popup(self, itterations, info):
        self.view.open_battle_popup(itterations, info)

    def get_prices(self):
        tank_list = self.model.s.get_tank_list()
        temp = []
        for _ in tank_list:
            temp.append(str(_.get_price()))
        return temp[:]

    def dialog(self, mode, dialog):
        self.model.open_dialog(mode, dialog)
