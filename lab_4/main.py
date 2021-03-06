from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable

# from Controller.myscreen import MyScreenController
# from Model.myscreen import MyScreenModel

from Controller import MyScreenController
from Model import MyScreenModel

from kivy.core.window import Window
from kivy.metrics import dp


class PassMVC(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model = MyScreenModel()
        self.controller = MyScreenController(self.model)

    def build(self):
        Window.size = (800, 600)
        return self.controller.get_screen()


PassMVC().run()
