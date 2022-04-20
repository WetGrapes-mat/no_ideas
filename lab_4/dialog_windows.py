import os

from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton


class DialogContent(BoxLayout):
    pass

class RenameDialogContent(DialogContent):
    pass

class AccountDialogContent(DialogContent):
    pass



class DialogWindow(MDDialog):
    def __init__(self, **kwargs):
        super().__init__(
            title=kwargs["title"],
            type="custom",
            content_cls=kwargs["content_cls"],
            buttons=[
                MDFlatButton(
                    text="OK",
                    theme_text_color="Custom",
                    on_release=self.close
                ),
            ],
        )
        self.mode = kwargs["mode"]
        self.model = kwargs["model"]

    def close(self, obj):
        self.dismiss()
        self.model.close_dialog()

class RenameWindow(DialogWindow):
    def __init__(self, **kwargs):
        super().__init__(
                title="Change nickname: ",
                content_cls=RenameDialogContent(),
                mode="rename",
                model=kwargs["model"],
        )


    def close(self, obj):
        self.dismiss()
        self.model.close_dialog(self.content_cls.ids.nickname.text)


class AccountWindow(DialogWindow):
    def __init__(self, **kwargs):
        super().__init__(
                title="Change acc: ",
                content_cls=AccountDialogContent(),
                mode="account",
                model=kwargs["model"],
        )


    def close(self, obj):
        self.dismiss()
        self.model.close_dialog(self.content_cls.ids.acc_name.text)




Builder.load_file(os.path.join(os.path.dirname(__file__), "dialog_windows.kv"))