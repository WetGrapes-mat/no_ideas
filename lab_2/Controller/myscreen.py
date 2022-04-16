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
    
    def change_account(self, data):
        self.model.read_data_from_file(path=data)
    
    def change_nickname(self, data):
        self.model.write_data_in_file(path=data)

    def start_buttle(self, tank):
        self.model.server.start_battle(tank, self)
