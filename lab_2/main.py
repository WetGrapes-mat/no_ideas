from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable

from Controller.myscreen import MyScreenController
from Model.myscreen import MyScreenModel

from kivy.core.window import Window
from kivy.metrics import dp

class PassMVC(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.table = MDDataTable(
            pos_hint={'center_x': 0.5, 'center_y': 0.565},
            size_hint=(0.9, 0.8),
            use_pagination=True,
            rows_num=7,
            column_data=[
                ("FIO", dp(50)),
                ("Group", dp(30)),
                ("Sick", dp(15)),
                ("Skip", dp(15)),
                ("Other", dp(15)),
                ("Total", dp(15)),
            ],
        )
        self.model = MyScreenModel(table=self.table)
        self.controller = MyScreenController(self.model)

    def build(self):
        Window.size = (800, 600)
        return self.controller.get_screen()


PassMVC().run()
