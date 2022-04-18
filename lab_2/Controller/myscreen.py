from View.myscreen import MyScreenView


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
        self.view = MyScreenView(controller=self, model=self.model)

    
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
        earned = self.model.start_battle(tank)
        self.prize_popup(earned)

    def buy_tank(self, tank):
        self.model.server.buy_tank(tank)

    def get_account_info(self):
        self.model.server.get_account_info()

    def prize_popup(self, earned):
        self.view.open_prize_popup(earned)

    def battle_popup(self, battle):
        self.view.open_battle_popup(battle)
