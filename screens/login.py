from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.app import App

class LoginMenu(Screen):
    def __init__(self, **kwargs):
        super(LoginMenu, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        self.username_input = TextInput(multiline=False)
        self.password_input = TextInput(multiline=False, password=True)
        self.message_label = Label(text='')
        layout.add_widget(Label(text='Username'))
        layout.add_widget(self.username_input)
        layout.add_widget(Label(text='Password'))
        layout.add_widget(self.password_input)
        layout.add_widget(Button(text='Login', on_press=self.do_login))
        layout.add_widget(Button(text='Register', on_press=self.do_register))
        layout.add_widget(Button(text='Back', on_press=self.go_back))
        layout.add_widget(self.message_label)
        self.add_widget(layout)

    def do_login(self, instance):
        app = App.get_running_app()
        app.login(self.username_input.text, self.password_input.text)

    def do_register(self, instance):
        app = App.get_running_app()
        app.register(self.username_input.text, self.password_input.text)

    def go_back(self, instance):
        App.get_running_app().show_main_menu()

    def update_message(self, message):
        self.message_label.text = message